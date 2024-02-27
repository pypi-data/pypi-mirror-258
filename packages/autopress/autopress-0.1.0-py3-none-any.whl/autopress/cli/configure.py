import click

DEFAULT_PROMPT = "Convert this method definition and docstring into a short description followed by a markdown table of parameters (columns are 'Name', 'Type', 'Default', 'Description') and a markdown table of returns (if applicable). If the docstring contains an example usage, then add it in the description. Use inline code for types and default values."

@click.group()
def configure_group():
    pass

@configure_group.command(
    name="configure",
    help="Set your configuration settings"
)
def configure():    
    from autopress.settings import write_env_file, getenv
    click.echo("Configuring autodoc")
    data = {}
    data["OPENAI_API_KEY"] = click.prompt("OpenAI Secret API Key", 
                                          type=str, 
                                          default=getenv("OPENAI_API_KEY", ""))
    data["INSTRUCTIONS"] = click.prompt("Instructions", 
                                        type=str, 
                                        default=getenv("INSTRUCTIONS", DEFAULT_PROMPT))
    path = write_env_file(data=data, name=".env")
    click.secho(f"✍️ Saving configuration at {path}", fg="green")
    click.echo("✅ Configuration completed.")
