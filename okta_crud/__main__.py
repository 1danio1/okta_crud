import click
import asyncio
from click.core import Context
from load_dotenv import load_dotenv
from okta.client import Client as OktaClient
from okta_crud import okta


load_dotenv()


@click.group()
@click.option("-i", "--instance", type=str, envvar="OKTA_INSTANCE", required=True, help="You Okta instance URL")
@click.option("-t", "--token", type=str, envvar="OKTA_API_TOKEN", required=True, help="Your Okta API token")
@click.pass_context
def cli(context: Context, instance: str, token: str) -> None:
    context.ensure_object(dict)
    config = {
        "orgUrl": instance,
        "token": token,
    }
    context.obj["client"] = OktaClient(config)


@cli.group()
@click.pass_context
def users(context: Context) -> None:
   pass


@users.command("list")
@click.pass_context
def list_users(context: Context) -> None:
    """Lists all users in the Okta instance"""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(okta.list_users(context.obj["client"]))
    

@users.command("get")
@click.pass_context
@click.option("-u", "--user", type=str, required=True, help="Okta user ID")
def get_user(context: Context, user: str) -> None:
    """Get all user information"""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(okta.get_user(context.obj["client"], user))


@users.command("create")
@click.pass_context
def create_user(context: Context) -> None:
    """Creates new user"""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(okta.create_user(context.obj["client"]))


@users.command("update")
@click.pass_context
@click.option("-u", "--user", type=str, required=True, help="Okta user ID")
def update_user(context: Context, user: str) -> None:
    """Updates user information"""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(okta.update_user(context.obj["client"], user))


if __name__ == "__main__":
    cli(obj={})