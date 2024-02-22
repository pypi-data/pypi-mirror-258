"""
This module is the main logic to sync objects from Azure AD to Databricks
"""
import argparse
import asyncio
import logging
import sys

from azure.identity import DefaultAzureCredential
from databricks.sdk import AccountClient

from azure_identity import AzureIdentity
from databricks_identity import DatabricksIdentity
from one_way_match import OneWayMatch
from sync_classes import SyncStatus
from yaml_parser import parse_yaml


def parse_arguments():
    """
    This function parses the following arguments provided by users:
    -f/--file: The path to the yaml file, which stores Azure AD group objects
    -j/--json: The path to the json file, which provides relations
               between Azure and Databricks
    -d/--delete: A boolean value indiciating if force delete is enabled
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        "-f",
        type=str,
        required=True,
        help="The path to the yaml file",
    )

    parser.add_argument(
        "--json",
        "-j",
        type=str,
        required=True,
        help="The path to the json file",
    )

    parser.add_argument(
        "--delete",
        "-d",
        help="If specified, you enable databricks identities to be deleted",
        action="store_true",
    )

    args = parser.parse_args()
    yaml_path = args.file
    json_path = args.json
    force_delete = args.delete

    return yaml_path, json_path, force_delete


def authenticate(json_path: str):
    """
    This function authenticates both Azure AD and Databricks
    Args:
        json_path (str): The path to the json file
    Return: two identities from Azure and Databricks
    """
    try:
        logging.info("Attempting to authenticate to Azure...")
        azure_credential = DefaultAzureCredential()
        azure_identity = AzureIdentity(azure_credential)
        logging.info("Authenticated to Azure.")
        logging.info("Attempting to authenticate to databricks...")
        db_account_client = AccountClient()
        databricks_identity = DatabricksIdentity(db_account_client, json_path)
        logging.info("Authenticated to databricks.")
        return (azure_identity, databricks_identity)

    except ValueError as ve:
        logging.error(ve)
        sys.exit()


def sync_users(owm: OneWayMatch, force_delete: bool):
    """
    This function checks users to be synced and execute the synchronization
    Args:
        owm: A OneWayMatch instance which stores all info from Databricks and Azure
        force_delete: A boolean value indiciating if force delete is enabled
    """
    logging.info("Compare and get users to be synced...")

    sync_users = owm.match_users()

    logging.info("#" * 80)
    logging.info("USERS TO SYNC")
    logging.info("#" * 80)
    for user in sync_users:
        logging.info(f"{user.azure_display_name}, {user.status}")
        user.sync_user_to_db(force_delete)


def sync_service_principals(owm: OneWayMatch, force_delete: bool):
    """
    This function checks service principals to be synced and execute the synchronization
    Args:
        owm: A OneWayMatch instance which stores all info from Databricks and Azure
        force_delete: A boolean value indiciating if force delete is enabled
    """
    logging.info("Compare and get service principals to be synced...")

    sync_sps = owm.match_service_principals()

    logging.info("#" * 80)
    logging.info("SERVICE PRINCIPALS TO SYNC")
    logging.info("#" * 80)
    for sp in sync_sps:
        logging.info(f"{sp.azure_display_name}, {sp.status}")
        sp.sync_sp_to_db(force_delete)


def sync_groups(owm: OneWayMatch, force_delete: bool):
    """
    This function checks groups to be synced and execute the synchronization
    Args:
        owm: A OneWayMatch instance which stores all info from Databricks and Azure
        force_delete: A boolean value indiciating if force delete is enabled
    """
    logging.info("Compare and get groups to be synced...")

    sync_groups = owm.match_groups()
    logging.info("#" * 80)
    logging.info("GROUPS TO SYNC:")
    logging.info("#" * 80)
    for group in sync_groups:
        logging.info(f"{group.azure_display_name}, {group.status}")

        if group.status == SyncStatus.TO_ADD:
            group.sync_group_add_empty()

    for group in sync_groups:
        group.sync_group_update(force_delete)


def main():
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.DEBUG,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    yaml_path, json_path, force_delete = parse_arguments()
    if force_delete:
        logging.info("Are you sure you want to force delete databricks objects? Y/N:")
        x = input()
        if x not in ['Y', 'y']:
            force_delete = False
            
    group_objects, exclude_objects = parse_yaml(yaml_path)
    azure_identity, databricks_identity = authenticate(json_path)

    logging.info("Calling Azure API...")

    azure_group_details = asyncio.run(
        azure_identity.get_azure_objects_with_exclude(group_objects, exclude_objects)
    )

    owm = OneWayMatch(azure_group_details, databricks_identity)

    sync_users(owm, force_delete)
    sync_service_principals(owm, force_delete)
    sync_groups(owm, force_delete)

    databricks_identity.write_json()


if __name__ == "__main__":
    main()
