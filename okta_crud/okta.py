import click

from okta.client import Client as OktaClient

async def list_users(okta_client: OktaClient) -> None:
    users, resp, err = await okta_client.list_users()
    click.secho("ID\tFirst Name\tLast Name\tEmail", bold=True)
    for user in users:
        click.echo(f"{user.id}\t{user.profile.first_name}\t{user.profile.last_name}\t{user.profile.email}")

async def get_user(okta_client: OktaClient, user_id: str) -> None:
    user, resp, err = await okta_client.get_user(user_id)
    if err:
        click.echo(err.message)
    else:
        click.secho(f"User ID:      {user.id}", bold=True)
        click.secho(f"User:         {user.profile.first_name} {user.profile.last_name} - {user.profile.email}")
        click.echo(f"Status:       {user.status}")
        click.echo(f"Last login:   {user.last_login}")
        click.echo(f"Last updated: {user.last_updated}")
        click.secho(f"Profile details:", bold=True)
        for attribute, value in user.profile.__dict__.items():
            click.echo(f"{attribute}: {value}")