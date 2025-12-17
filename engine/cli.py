#!/usr/bin/env python3
"""CLI interface for remediation engine."""

import click

@click.group()
def cli():
    """Evolutionary Remediation Engine CLI."""
    pass

@cli.command()
@click.option('--repo', required=True)
def scan(repo: str):
    """Scan repository for applicable patterns."""
    click.echo(f"Scanning {repo}...")

@cli.command()
@click.option('--repo', required=True)
def fix(repo: str):
    """Generate fixes."""
    click.echo(f"Generating fixes for {repo}...")

if __name__ == '__main__':
    cli()
