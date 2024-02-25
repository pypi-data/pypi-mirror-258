# Standard modules
from typing import Any, Dict, List, Union

# Third-party modules
import click
from rich import box
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


# Product modules
from .utils import print_to_string
from .client import send_request
from .datamodels.datamodels.api import InferenceDeploymentStatus


def get_deployment(inf_id: str) -> Dict[str, Any]:
    console = Console()

    with console.status(f"[bold green]Getting deployment with inf_id {inf_id}...") as status:

        resp = send_request("GET", f"/sg_inf/{inf_id}")

    if resp.status_code == 204:
        click.echo(click.style(f"Deployment with inf_id {inf_id} not found", fg="red"), err=True)
        exit()

    elif resp.status_code != 200:
        click.echo(click.style(f"Could not fetch deployment", fg="red"), err=True)
        exit()

    deployment = resp.json()
    return deployment


def get_deployments(should_exist: bool = True):
    console = Console()

    with console.status("[bold green]Getting existing deployments...") as status:

        resp = send_request("GET", "/sg_inf/list")

    if resp.status_code == 204:
        if should_exist:
            click.echo(click.style(f"No deployments found. Create one with 'scalegen infer create'", fg="blue"), err=should_exist)
        return []

    elif resp.status_code != 200:
        click.echo(click.style(f"Could not fetch deployments", fg="red"), err=True)
        exit()

    deployments = resp.json()
    deployments.sort(key=lambda dep: dep['name'])

    return deployments


def print_inference_deployments(deployments: List[Dict[str, Any]], show_inf_ids: bool = False, table_title: str = "Inference Deployments", plain: bool = False):
    table = Table(
        show_header = True,
        # header_style='bold #2070b2',
        # title='[bold] Jobs',
        title=table_title,
        box = None if plain else box.DOUBLE_EDGE
    )

    col_names = ['Name', 'Model', 'Allow Spot Instances', "Current Price Per Hour", "Status", "API Gateway"]
    if show_inf_ids:
        col_names.insert(0, "Inference ID")
        
    for col in col_names: 
        table.add_column(col)

    for depl in deployments:
        row = [depl["name"], depl["model"], str(depl["allow_spot_instances"]), str(depl["current_price_per_hour"]), depl["status"], depl["link"]]
        if row[-1] is None:
            row[-1] = "Unavailable"
        else:
            row[-1] = print_to_string(
                f"[link={depl['link'] + '/inference'}]Inference link[/link]\n"
                f"[link={depl['link'] + '/metrics'}]Metrics link[/link]",
                end=''
            )

        if show_inf_ids:
            row.insert(0, depl["id"])

        table.add_row(*row)

    console = Console()
    
    if table.row_count <= 15:
        console.print(table, justify='left')
    else:
        with console.pager():
            console.print(table, justify='left')


@click.group(name='infer', chain=True)
def infer():
    """
    Commands for managing an inference deployment for ScaleGen
    """
    pass


@infer.command('create')
@click.option('--model', type=click.STRING, required=True)
@click.option('--max_price_per_hour', type=click.INT, required=False, default=20)
@click.option('--allow_spot_instances', type=click.BOOL, required=False, default=False)
@click.option('--name', type=click.STRING, required=True)
@click.option('--hf_token', type=click.STRING, required=False)
@click.option('--logs_bucket', type=click.STRING, required=True)
@click.option('--min_workers', type=click.INT, required=False, default=0)


@click.option('-f', '--force', is_flag=True)
@click.option("-q", "--quiet", is_flag=True)
def create_impl(model, max_price_per_hour, allow_spot_instances, name, hf_token, logs_bucket, min_workers, force, quiet):
    """
    Create an inference deployment
    """

    # Get existing deployments
    deployments = get_deployments(should_exist=False)
    
    # Check if there is already a deployment with the same model
    similar_deployments = list(map(lambda x: x["name"], filter(lambda x: x["model"] == model, deployments)))
    if similar_deployments and not force:
        # If exists, Warn the user
        if not click.confirm(click.style(f"This model is already deployed with name(s): {similar_deployments}. Do you want to continue?", fg="yellow")):
            exit()
    

    # Make request to P-API
    data = {
        "name": name,
        "model": model,
        "hf_token": hf_token,
        "allow_spot_instances": allow_spot_instances,
        "max_price_per_hour": max_price_per_hour,
        "logs_bucket_s3": logs_bucket,
        
        # "artifactsDestination": {
        #     "name": "string",
        #     "filter": "string"
        # },
        
        "initial_worker_config": {
            "min_workers": min_workers,
            # "initial_workers_gpu": "string",
            # "initial_workers_gpu_num": 0,
            # "use_same_gpus_when_scaling": False
        },
        # "autoscaling_config": {
        #     "lower_allowed_latency_sec": 1,
        #     "scale_to_zero_timeout_min": 30,
        #     "scaling_timeout_min": 20,
        #     "time_window_minutes": 5,
        #     "upper_allowed_latency_sec": 4
        # }
    }

    console = Console()

    with console.status("[bold green]Creating new deployment...") as status:
        resp = send_request("POST", "/sg_inf/create", data=data)
        inf_id = ""

    if resp.status_code == 200:
        resp_data = resp.json()
        inf_id = resp_data['message']['inf_id'] # P-API returns dict for CREATE request
        click.echo(click.style(f"\nCreated deployment - Id: {inf_id}", fg='green'))
    
    elif resp.status_code == 500:
        resp_data = resp.content.decode('utf-8')
        click.echo(click.style(f"\nSomething went wrong: {resp_data}. Please try creating deployment later", fg="red"), err=True)
        return
    
    else:
        try:
            resp_data = resp.json()
            click.echo(click.style(f"\nCouldn't not create deployment: {resp_data}", fg='red'), err=True)
        except Exception as e:
            click.echo(click.style(f"\nCouldn't not create deployment", fg="red"), err=True)
        return
       
    # Exit if quiet was passed
    if not quiet:
        print_inference_deployments([get_deployment(inf_id)], show_inf_ids=True, table_title="New Deployment Added")


@infer.command('start')
@click.option('--name', type=click.STRING, required=True)
@click.option('--inf_id', type=click.STRING, required=False)
def start_impl(name, inf_id):
    """
    Allows user to make the InfereceDeployment Active in case 
    its been scaled to zero because of no-requests (status is INACTIVE)
    """

    def _check_if_deployment_already_started(inf_id: str):
        console = Console()

        with console.status(f"[bold green]Getting deployment with inf_id {inf_id}...") as status:

            resp = send_request('GET', f'/sg_inf/{inf_id}/gpu_nodes_ips')
            resp_json = ""

        if resp.status_code == 200:
            # Fetched GPU nodes successfully
            resp_data = resp.json()
            return True
        elif resp.status_code == 500:
            resp_data = resp.content.decode('utf-8')
            click.echo(click.style(f"\nSomething went wrong: {resp_data}. Please try fetching deployment GPU nodes later", fg="red"), err=True)
            return False
        else:
            try:
                resp_data = resp.json()
                click.echo(click.style(f"\nCould not fetch deployment GPU nodes: {resp_data}", fg="red"), err=True)
            except Exception as e:
                click.echo(click.style(f"\nCould not fetch deployment GPU nodes", fg="red"), err=True)
            return False

        if len(resp_json) > 0:
            # If there are already existing GPU nodes, Warn the user
            if not click.confirm(click.style(f"Deployment {inf_id} already running with {len(resp_json)} GPU nodes. Do you want to continue scaling up?", fg="yellow")):
                exit()

    def _start_impl(inf_id: str):
        if not _check_if_deployment_already_started(inf_id):
            return

        console = Console()

        with console.status(f"[bold green]Scaling deployment with inf_id {inf_id}...") as status:

            resp = send_request('POST', f'/sg_inf/{inf_id}/scale/up')

        if resp.status_code == 200:
            resp_data = resp.json()
            click.echo(click.style(f"\nScaled deployment up with Id: {inf_id} successfully", fg='green'))
        elif resp.status_code == 500:
            resp_data = resp.content.decode('utf-8')
            click.echo(click.style(f"\nSomething went wrong: {resp_data}. Please try scaling deployment later", fg="red"), err=True)
            return
        else:
            try:
                resp_data = resp.json()
                click.echo(click.style(f"\nCould not scale up deployment: {resp_data}", fg='red'), err=True)
            except Exception as e:
                click.echo(click.style(f"\nCould not scale up deployment", fg='red'), err=True)
            return

    # Get existing deployments
    deployments = get_deployments(should_exist=True)

    # Collect inf_id list
    inf_ids = list(map(lambda x: x["id"], filter(lambda x: x["name"] == name, deployments)))

    # In case user specified inf_id
    if inf_id is not None:
        if inf_id in inf_ids: # if name and inf_id match
            _start_impl(inf_id=inf_id)
            exit()
        else: # if name and inf_id do not match
            click.echo(click.style(f"Could not start deployment: name ({name}) and inf_id ({inf_id}) do not match!", fg="red"), err=True)
            print_inference_deployments(deployments, show_inf_ids=True)
            exit()

    # If there is more than one inference with given name
    if len(inf_ids) > 1:
        click.echo(
            click.style(
                f"Could not start deployment: more than one inference found with the name: {name}\n"
                "Specify --inf_id to start particular inference", 
                fg="red"), 
            err=True
        )
        print_inference_deployments(deployments, show_inf_ids=True)
        exit()

    # If there are no inferences with given name
    if len(inf_ids) == 0:
        click.echo(click.style(f"Could not start deployment: {name} does not exist", fg="red"), err=True)
        click.echo(f"Available deployments:\n")
        print_inference_deployments(deployments, show_inf_ids=False)
        exit()

    _start_impl(inf_id=inf_ids[0])


@infer.command('delete')
@click.argument("inf-id", type=click.STRING, required=True)
def delete_impl(inf_id):
    """
    Delete an inference deployment
    """

    console = Console()

    with console.status(f"[bold green]Deleting deployment with inf_id {inf_id}...") as status:
        
        resp = send_request('DELETE', f'/sg_inf/{inf_id}')

    if resp.status_code == 200:
        resp_data = resp.json()
        click.echo(click.style(f"\nDelete request for deployment with id: {inf_id} is successful", fg='green'))
    elif resp.status_code == 500:
        resp_data = resp.content.decode('utf-8')
        click.echo(click.style(f"\nSomething went wrong: {resp_data}. Please try deleting deployment later", fg="red"), err=True)
        return
    else:
        try:
            resp_data = resp.json()
            click.echo(click.style(f"\nCould not delete deployment: {resp_data}", fg='red'), err=True)
        except Exception as e:
            click.echo(click.style(f"\nCould not delete deployment", fg='red'), err=True)
        return


@infer.command('list')
@click.option('-v', '--verbose', is_flag=True)
@click.option('-p', '--plain', is_flag=True)

def list_impl(verbose, plain):
    """
    Print the list of existing inference deployments
    """
    
    # Get existing deployments
    deployments = get_deployments(should_exist=True)

    print_inference_deployments(deployments, show_inf_ids=verbose, plain=plain)


@infer.command('view')
@click.argument("inf-id", type=click.STRING, required=True)
def view_impl(inf_id):
    """
    Print information about a single inference deployment
    """

    console = Console()
    inf_dep = get_deployment(inf_id)

    markdown_content = f"[bold][orange_red1]ID[/orange_red1] : [cyan]{inf_dep['id']}[/cyan]\n"
    markdown_content += f"[orange_red1]Name[/orange_red1] : [yellow]{inf_dep['name']}[/yellow]\n"
    markdown_content += f"[orange_red1]Status[/orange_red1] : [yellow]{inf_dep['status']}[/yellow]\n"
    markdown_content += f"[orange_red1]Cost[/orange_red1] : [yellow]$ {round(inf_dep['current_price_per_hour'], 3)}[/yellow]\n"

    console.print(Panel(markdown_content))
