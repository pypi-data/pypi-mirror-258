# SPDX-FileCopyrightText: 2024 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import os

import click
from tgclients.config import DEV_SERVER, PROD_SERVER
from tgclients import (
    TextgridConfig,
    TextgridAuth,
    TextgridSearch,
    TextgridCrud,
    TextgridCrudRequest,
)

import xml.etree.ElementTree as ET
import re
from xml.dom.minidom import parse
from concurrent.futures import ThreadPoolExecutor, as_completed


class TGclient(object):
    def __init__(self, sid, server):
        self.sid = sid
        self.config = TextgridConfig(server)
        self.tgauth = TextgridAuth(self.config)
        self.tgsearch = TextgridSearch(self.config, nonpublic=True)
        self.crud_req = TextgridCrudRequest(self.config)
        self.crud = TextgridCrud(self.config)


pass_tgclient = click.make_pass_decorator(TGclient)


@click.group()
@click.option(
    "-s",
    "--sid",
    default=lambda: os.environ.get("TEXTGRID_SID", ""),
    required=True,
    help="A textgrid session ID. Defaults to environment variable TEXTGRID_SID",
)
@click.option(
    "--server",
    default=PROD_SERVER,
    help="the server to use, defaults to " + PROD_SERVER,
)
@click.option("--dev", is_flag=True, help="use development system: " + DEV_SERVER)
@click.pass_context
def cli(ctx, sid, server, dev):
    """Helper cli tool to list or create TextGrid projects"""

    authz = "textgrid-esx2.gwdg.de"
    if dev:
        server = DEV_SERVER
        authz = "textgrid-esx1.gwdg.de"

    if sid == "":
        click.secho(
            f"""Please provide a textgrid session ID. Get one from
        {server}/1.0/Shibboleth.sso/Login?target=/1.0/secure/TextGrid-WebAuth.php?authZinstance={authz}
        and add with '--sid' or provide environment parameter TEXTGRID_SID
        """,
            fg="red",
        )
        exit(0)

    ctx.obj = TGclient(sid, server)


@cli.command()
@click.option(
    "--urls", "as_urls", help="list projects as urls for staging server", is_flag=True
)
@pass_tgclient
def list(client, as_urls):
    """List existing projects."""

    projects = client.tgauth.list_assigned_projects(client.sid)

    for project_id in projects:
        desc = client.tgauth.get_project_description(project_id)
        if as_urls:
            click.secho(
                f"https://staging.textgridrep.org/project/{project_id} : {desc.name}"
            )
        else:
            click.secho(f"{project_id} : {desc.name}")


@cli.command()
@click.option("-d", "--description", help="project description")
@click.argument("name")
@pass_tgclient
def create(client, name, description):
    """Create new project with name "name"."""

    project_id = client.tgauth.create_project(client.sid, name, description)
    click.secho(f"created new project with ID: {project_id}")


@cli.command()
@click.argument("project_id")
@pass_tgclient
def contents(client, project_id):
    """list contents of project"""

    contents = client.tgsearch.search(
        filters=["project.id:" + project_id], sid=client.sid, limit=100
    )

    click.echo(f"project {project_id} contains {contents.hits} files:")

    for tgobj in contents.result:
        title = tgobj.object_value.generic.provided.title
        tguri = tgobj.object_value.generic.generated.textgrid_uri.value

        click.echo(f" - {tguri}: {title}")


@cli.command()
@click.option(
    "--clean",
    "do_clean",
    help="call clean automatically if project not empty",
    is_flag=True,
)
@click.option(
    "--limit",
    help="how much uris to retrieve for deletion in one query (if called with --clean) (Default: 100)",
    default=100,
)
@click.confirmation_option(prompt="Are you sure you want to delete the project?")
@click.argument("project_id")
@pass_tgclient
def delete(client, project_id, do_clean, limit):
    """Delete project with project id "project_id"."""

    contents = client.tgsearch.search(
        filters=["project.id:" + project_id], sid=client.sid
    )
    if int(contents.hits) > 0:
        click.echo(
            f"project {project_id} contains {contents.hits} files. Can not delete project (clean or force with --clean)"
        )
        if do_clean:
            clean_op(client, project_id, limit)
        else:
            exit(0)

    res = client.tgauth.delete_project(client.sid, project_id)
    click.secho(f"deleted, status: {res}")


@cli.command()
@click.argument("project_id")
@click.option(
    "--limit",
    help="how much uris to retrieve for deletion in one query (Default: 100)",
    default=100,
)
@click.option(
    "--threaded", help="use multithreading for crud delete requests", is_flag=True
)
@pass_tgclient
def clean(client, project_id, limit, threaded):
    """Delete all content from project with project id "project_id"."""

    clean_op(client, project_id, limit, threaded)


def clean_op(
    client: TGclient, project_id: str, limit: int = 100, threaded: bool = False
):
    """delete all objects belonging to a given project id

    Args:
        client (TGClient): instance of tglcient
        project_id (str): the project ID
        limit (int): how much uris to retrieve for deletion in one query
        threaded (bool): wether to use multiple threads for deletion
    """

    contents = client.tgsearch.search(
        filters=["project.id:" + project_id], sid=client.sid, limit=limit
    )

    click.echo(f"project {project_id} contains {contents.hits} files:")

    for tgobj in contents.result:
        title = tgobj.object_value.generic.provided.title
        tguri = tgobj.object_value.generic.generated.textgrid_uri.value

        click.echo(f" - {tguri}: {title}")

    if int(contents.hits) > limit:
        click.echo(f" ...and ({int(contents.hits) - limit}) more objects")

    if not click.confirm("Do you want to delete all this objects"):
        exit(0)
    else:

        with click.progressbar(
            length=int(contents.hits),
            label="deleting object",
            show_eta=True,
            show_pos=True,
            item_show_func=lambda a: a,
        ) as bar:

            # iterate with paging
            nextpage = True
            while nextpage:

                if not threaded:
                    for tgobj in contents.result:
                        result = _crud_delete_op(client, tgobj)
                        bar.update(1, result)
                else:
                    with ThreadPoolExecutor(max_workers=limit) as ex:
                        futures = [
                            ex.submit(_crud_delete_op, client, tgobj)
                            for tgobj in contents.result
                        ]

                        for future in as_completed(futures):
                            result = future.result()
                            bar.update(1, result)

                if int(contents.hits) < limit:
                    # stop if there are no more results left
                    nextpage = False
                else:
                    # get next page of results from tgsearch
                    contents = client.tgsearch.search(
                        filters=["project.id:" + project_id],
                        sid=client.sid,
                        limit=limit,
                    )


def _crud_delete_op(client, tgobj):
    tguri = tgobj.object_value.generic.generated.textgrid_uri.value
    title = tgobj.object_value.generic.provided.title
    res = client.crud.delete_resource(client.sid, tguri)
    if res.status_code == 204:
        return f"deleted {tguri}: {title}"
    else:
        return f"error deleting {tguri}: {title}"


@cli.command()
@click.argument("project_id")
@click.argument("the_data", type=click.File("rb"))
@click.argument("metadata", type=click.File("rb"))
@pass_tgclient
def put(client, project_id, the_data, metadata):
    """put a file with metadata online"""

    res = client.crud_req.create_resource(
        client.sid, project_id, the_data, metadata.read()
    )
    click.echo(res)


@cli.command()
@click.argument("textgrid_uri")
@click.argument("the_data", type=click.File("rb"))
@pass_tgclient
def update_data(client, textgrid_uri, the_data):
    """update a file"""

    metadata = client.crud.read_metadata(textgrid_uri, client.sid)
    client.crud.update_resource(client.sid, textgrid_uri, the_data, metadata)

    metadata = tgc.read_metadata(textgrid_uri, sid)
    tgc.update_resource(sid, textgrid_uri, the_data, metadata)


@cli.command()
@click.argument("imex", type=click.File("rb"))
@click.argument("folder_path")
@click.option(
    "--newrev", "make_revision", help="to update data as new revisions", is_flag=True
)
@pass_tgclient
def update_imex(
    client, imex, folder_path: str, server=DEV_SERVER, make_revision: bool = True
):
    """update from imex, argument 1 is the IMEX file, argument 2 the path where the data
    is located, as the imex has only relative paths.
    """

    namespaces = {"ore": "http://www.openarchives.org/ore/terms/"}

    imexXML = parse(imex)

    importObjects = imexXML.getElementsByTagName("importObject")
    with click.progressbar(importObjects) as bar:
        for importObject in bar:
            textgrid_uri = importObject.getAttribute("textgrid-uri")
            with open(
                folder_path + "/" + importObject.getAttribute("local-data"), "rb"
            ) as the_data:
                metadata = client.crud.read_metadata(textgrid_uri, client.sid)
                # rev uri, because we may have base uris, but metadata will have latest rev
                revision_uri = (
                    metadata.object_value.generic.generated.textgrid_uri.value
                )

                # aggregations contains local path on disk, but we need the textgrid-baseuri instead
                if "tg.aggregation" in metadata.object_value.generic.provided.format:
                    rdf_resource = (
                        "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource"
                    )
                    the_dataXML = ET.parse(the_data)
                    the_dataXML_root = the_dataXML.getroot()
                    title = metadata.object_value.generic.provided.title[0]
                    click.echo(f'\nrewriting {revision_uri}("{title}"):')
                    for ore_aggregates in the_dataXML_root.findall(
                        ".//ore:aggregates", namespaces
                    ):
                        resource_path = ore_aggregates.attrib[rdf_resource]
                        # we assume that the path has the ending "tguri.revision.file-extension"
                        # split by the . and use the 3rd part from the end as baseuri
                        resource_path_array = resource_path.split(".")
                        try:
                            baseuri = resource_path_array[len(resource_path_array) - 3]
                        except:
                            pass
                        else:
                            resource_URI = "textgrid:" + baseuri
                            ore_aggregates.set(rdf_resource, resource_URI)
                            click.echo(f"  {resource_path}  -> {resource_URI}")
                    the_data = ET.tostring(
                        the_dataXML_root, encoding="utf8", method="xml"
                    )

                client.crud.update_resource(
                    client.sid,
                    revision_uri,
                    the_data,
                    metadata,
                    create_revision=make_revision,
                )
