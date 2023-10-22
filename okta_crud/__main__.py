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
def cli(ctx: Context, instance: str, token: str) -> None:
    ctx.ensure_object(dict)
    config = {
        "orgUrl": instance,
        "token": token,
    }
    ctx.obj["client"] = OktaClient(config)

@cli.group()
@click.pass_context
def users(ctx: Context) -> None:
   pass

@users.command("list")
@click.pass_context
def list_users(ctx: Context) -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(okta.list_users(ctx.obj["client"]))
    
@users.command("get")
@click.pass_context
@click.option("-u", "--user", type=str, required=True, help="Okta user ID")
def get_user(ctx: Context, user: str) -> None:
    """Get all user information"""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(okta.get_user(ctx.obj["client"], user))

if __name__ == "__main__":
    cli(obj={})