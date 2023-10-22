import click
from okta.client import Client as OktaClient
from okta_crud.utils import camel

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


async def create_user(okta_client: OktaClient) -> None:
    schema, resp, err = await okta_client.get_user_schema("default", keep_empty_params=True)
    click.secho("Input user attributes", bold=True)
    profile_attributes = {}
    for attribute in schema.definitions.base.properties.__dict__.items():
        attribute_camel = camel(attribute[0])
        required = ""
        if attribute_camel in schema.definitions.base.required:
            required = "*"
        value = input(f"{attribute_camel}{required} []: ").strip()
        if value:
            profile_attributes[attribute_camel] = value
    for attribute in schema.definitions.custom.properties.items():
        required = ""
        if attribute[0] in schema.definitions.custom.required:
            required = "*"
        value = input(f"{attribute[0]}{required} []: ").strip()
        if value:
            profile_attributes[attribute[0]] = value

    click.echo("\n\n")
    click.secho("User attributes to create:", bold=True)
    for attribute, value in profile_attributes.items():
        click.echo(f"{attribute}: {value}")
    
    click.echo("\n\n")
    activate = False
    activate_input = input("Do you want to activate user immediately? [y/N]: ")
    if activate_input.lower().strip() == "y":
        activate = True

    click.echo("\n\n")
    password = ""
    password_choice = input("Do you want to set password? [y/N]: ")
    if password_choice.lower().strip() == "y":
        password = input("Password [empty to cancel]: ")

    click.echo("\nCreating user...\n")
    body = {"profile": profile_attributes}
    if password:
        body["credentials"] = {"password": {"value": password}}
    query_params={}
    if activate:
        query_params = {"activate": "true"}

    user, resp, err = await okta_client.create_user(body, query_params=query_params)
    if err:
        click.echo(err)
    else:
        click.echo(f"User created. ID: {user.id}\t {user.profile.first_name} {user.profile.last_name} - {user.profile.email}")


async def update_user(okta_client: OktaClient, user_id: str) -> None:
    user, resp, err = await okta_client.get_user(user_id)
    update_profile = input("Update profile attributes? [y/N]: ")
    if update_profile.lower().strip() == "y":
        click.secho("Change attribute values [whitespace to clear the value]", bold=True)
        for attribute, value in user.profile.__dict__.items():
            if not value:
                value = ""
            value_input = input(f"{attribute} [{value}]: ")
            if not value_input.isspace():
                value_input = value_input.strip()

            if value and value_input.isspace():
                setattr(user.profile, attribute, "")
            elif value_input.strip():
                setattr(user.profile, attribute, value_input.strip())

    click.echo("\n\n")
    password = ""
    update_password = input("Update password? [y/N]: ")
    if update_password.lower().strip() == "y":
        password = input("Password [empty to cancel]: ")
        user.credentials.password.value = password

    click.echo("Updating user...\n")
    updated_user, resp, err = await okta_client.update_user(user_id, user)
    click.echo("User updated...\n")