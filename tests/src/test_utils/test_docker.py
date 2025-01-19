from unittest.mock import patch, call
import pytest
from src.utils.docker import Docker

### DOCKER COMPOSE ###

@patch("src.utils.docker.platform.system", return_value="Windows")
@patch("src.utils.docker.os.path.exists", return_value=True)
@patch("src.utils.docker.Command.run")
def test_compose_build_with_npm_installed_and_reinstall_true(
    mock_run, _mock_exists, _mock_platform):
    Docker.Compose.build("my/frontend", npm=True, reinstall=True)
    expected_calls = [
        call(["npm.cmd", "--version"], inherit_environment=True),
        call(["npm.cmd", "install"], directory="my/frontend", inherit_environment=True),
        call(["npm.cmd", "run", "build"], directory="my/frontend", inherit_environment=True)
    ]
    mock_run.assert_has_calls(expected_calls)
    assert mock_run.call_count == 3

@patch("src.utils.docker.platform.system", return_value="Windows")
@patch("src.utils.docker.os.path.exists", return_value=True)
@patch("src.utils.docker.Command.run")
def test_compose_build_with_npm_installed_and_reinstall_false(
    mock_run, _mock_exists, _mock_platform):
    Docker.Compose.build("my/frontend", npm=True, reinstall=False)
    expected_calls = [
        call(["npm.cmd", "--version"], inherit_environment=True),
        call(["npm.cmd", "run", "build"], directory="my/frontend", inherit_environment=True)
    ]
    mock_run.assert_has_calls(expected_calls)
    assert mock_run.call_count == 2

@patch("src.utils.docker.platform.system", return_value="Windows")
@patch("src.utils.docker.Command.run", side_effect=Exception("NPM not installed"))
def test_compose_build_with_npm_not_installed(mock_run, _mock_platform):
    with pytest.raises(Exception) as exc_info:
        Docker.Compose.build("my/frontend", npm=True)
    assert "NPM is not installed." in str(exc_info.value)
    mock_run.assert_called_once_with(["npm.cmd", "--version"], inherit_environment=True)

@patch("src.utils.docker.platform.system", return_value="Linux")
@patch("src.utils.docker.Command.run")
def test_compose_build_without_npm(mock_run, _mock_platform):
    Docker.Compose.build("my/backend", npm=False)
    mock_run.assert_called_once_with(["docker-compose", "build"], directory="my/backend")

@patch("src.utils.docker.Command.run")
def test_compose_up_with_npm(mock_run):
    Docker.Compose.up("my/frontend", npm=True)
    expected_calls = [
        call(["docker-compose", "down"], directory="my/frontend"),
        call(["docker-compose", "up", "webclient-prod", "-d"], directory="my/frontend")
    ]
    mock_run.assert_has_calls(expected_calls)
    assert mock_run.call_count == 2

@patch("src.utils.docker.Command.run")
def test_compose_up_without_npm(mock_run):
    Docker.Compose.up("my/backend", npm=False)
    expected_calls = [
        call(["docker-compose", "down"], directory="my/backend"),
        call(["docker-compose", "up", "-d", "--build"], directory="my/backend")
    ]
    mock_run.assert_has_calls(expected_calls)
    assert mock_run.call_count == 2

@patch("src.utils.docker.platform.system", return_value="Linux")
@patch("src.utils.docker.os.path.exists", side_effect=lambda path: path.endswith('build'))
@patch("src.utils.docker.Command.run")
def test_compose_build_npm_reinstall_false_build_not_exists(mock_run, _mock_exists, _mock_platform):
    Docker.Compose.build("my/frontend", npm=True, reinstall=False)
    expected_calls = [
        call(["npm", "--version"], inherit_environment=True),
        call(["npm", "run", "build"], directory="my/frontend", inherit_environment=True)
    ]
    mock_run.assert_has_calls(expected_calls)
    assert mock_run.call_count == 2

@patch("src.utils.docker.platform.system", return_value="Linux")
@patch("src.utils.docker.os.path.exists", side_effect=lambda path: path.endswith('build'))
@patch("src.utils.docker.Command.run")
def test_compose_build_npm_reinstall_true_build_not_exists(mock_run, _mock_exists, _mock_platform):
    Docker.Compose.build("my/frontend", npm=True, reinstall=True)
    expected_calls = [
        call(["npm", "--version"], inherit_environment=True),
        call(["npm", "install"], directory="my/frontend", inherit_environment=True),
        call(["npm", "run", "build"], directory="my/frontend", inherit_environment=True)
    ]
    mock_run.assert_has_calls(expected_calls)
    assert mock_run.call_count == 3

@patch("src.utils.docker.Command.run")
def test_compose_down_success(mock_run):
    Docker.Compose.down("my/project")
    mock_run.assert_called_once_with(["docker-compose", "down"], directory="my/project")

@patch("src.utils.docker.Command.run")
def test_compose_status(mock_run):
    Docker.Compose.status("my/project")
    mock_run.assert_called_once_with(["docker-compose", "ps"], directory="my/project")

@patch("src.utils.docker.Command.run")
def test_compose_logs(mock_run):
    Docker.Compose.logs("my/project")
    mock_run.assert_called_once_with(
        ["docker-compose", "logs", "-f"],
        directory="my/project",
        raise_exception=False
    )

@patch("src.utils.docker.Command.run")
@patch("src.utils.docker.os.path.exists", return_value=False)
@patch("src.utils.docker.platform.system", return_value="Linux")
def test_compose_build_npm_install_failure(_mock_platform, _mock_exists, mock_run):
    mock_run.side_effect = [None, Exception("NPM install failed")]
    with patch("builtins.print") as mock_print:
        Docker.Compose.build("my/frontend", npm=True, reinstall=True)
        mock_run.assert_any_call(["npm", "--version"], inherit_environment=True)
        mock_run.assert_any_call(
            ["npm", "install"],
            directory="my/frontend",
            inherit_environment=True
        )
        mock_print.assert_any_call("Failed to run NPM install: NPM install failed")
        mock_print.assert_any_call("/build exists: False")

@patch("src.utils.docker.Command.run")
@patch("src.utils.docker.platform.system", return_value="Linux")
def test_compose_build_npm_build_failure(_mock_platform, mock_run):
    mock_run.side_effect = [None, None, Exception("NPM build failed")]
    with patch("builtins.print") as mock_print:
        Docker.Compose.build("my/frontend", npm=True, reinstall=False)
        mock_run.assert_any_call(["npm", "--version"], inherit_environment=True)
        mock_run.assert_any_call(
            ["npm", "run", "build"],
            directory="my/frontend",
            inherit_environment=True
        )
        mock_print.assert_any_call("Running npm run build...")
        mock_print.assert_any_call("Failed to run NPM build: NPM build failed")

@patch("src.utils.docker.Command.run", side_effect=Exception("Docker build failed"))
@patch("src.utils.docker.platform.system", return_value="Linux")
def test_compose_build_docker_failure(_mock_platform, mock_run):
    with patch("builtins.print") as mock_print:
        Docker.Compose.build("my/backend", npm=False)
        mock_run.assert_called_once_with(
            ["docker-compose", "build"],
            directory="my/backend"
        )
        mock_print.assert_any_call("Building the Docker image...")
        mock_print.assert_any_call("Failed to build the Docker image: Docker build failed")

@patch("src.utils.docker.Docker.Compose.up")
@patch("src.utils.docker.Docker.Compose.down")
def test_compose_restart(mock_down, mock_up):
    Docker.Compose.restart("my/project")
    mock_down.assert_called_once_with("my/project")
    mock_up.assert_called_once_with("my/project")

### DOCKER COMPOSE COMBINED ###

@patch("src.utils.docker.Command.run")
def test_compose_combined_build(mock_run):
    Docker.Compose.Combined.build(
        "my/project", ["docker-compose.yml", "docker-compose.override.yml"])
    expected_command = ["docker-compose", "-f",
                        "docker-compose.yml", "-f", "docker-compose.override.yml", "build"]
    mock_run.assert_called_once_with(
        expected_command, directory="my/project", raise_exception=False)

@patch("src.utils.docker.Command.run")
def test_compose_combined_up(mock_run):
    Docker.Compose.Combined.up(
        "my/project",
        ["docker-compose.yml", "docker-compose.override.yml"])
    expected_command = ["docker-compose", "-f", "docker-compose.yml",
                        "-f", "docker-compose.override.yml", "up", "-d"]
    mock_run.assert_called_once_with(
        expected_command, directory="my/project", raise_exception=False)

@patch("src.utils.docker.Command.run")
def test_compose_combined_down(mock_run):
    Docker.Compose.Combined.down(
        "my/project",
        ["docker-compose.yml", "docker-compose.override.yml"])
    expected_command = ["docker-compose", "-f",
                        "docker-compose.yml", "-f",
                        "docker-compose.override.yml", "down"]
    mock_run.assert_called_once_with(
        expected_command, directory="my/project", raise_exception=False)

@patch("src.utils.docker.Command.run")
def test_compose_combined_status(mock_run):
    Docker.Compose.Combined.status(
        "my/project",
        ["docker-compose.yml", "docker-compose.override.yml"])
    expected_command = ["docker-compose",
                        "-f", "docker-compose.yml",
                        "-f", "docker-compose.override.yml", "ps"]
    mock_run.assert_called_once_with(
        expected_command, directory="my/project", raise_exception=False)

@patch("src.utils.docker.Command.run")
def test_compose_combined_logs(mock_run):
    Docker.Compose.Combined.logs(
        "my/project",
        ["docker-compose.yml", "docker-compose.override.yml"])
    expected_command = ["docker-compose", "-f",
                        "docker-compose.yml", "-f",
                        "docker-compose.override.yml", "logs", "-f"]
    mock_run.assert_called_once_with(
        expected_command, directory="my/project", raise_exception=False)

@patch("src.utils.docker.Command.run")
def test_combine_with_empty_filenames(mock_run):
    Docker.Compose.Combined.build("my/project", [])
    expected_command = ["docker-compose", "build"]
    mock_run.assert_called_once_with(
        expected_command,
        directory="my/project",
        raise_exception=False
    )

@patch("src.utils.docker.Command.run")
def test_combine_methods_with_multiple_files(mock_run):
    filenames = ["docker-compose.yml", "docker-compose.override.yml", "docker-compose.prod.yml"]
    Docker.Compose.Combined.up("my/project", filenames)
    expected_command = [
        "docker-compose",
        "-f", "docker-compose.yml",
        "-f", "docker-compose.override.yml",
        "-f", "docker-compose.prod.yml",
        "up", "-d"
    ]
    mock_run.assert_called_with(expected_command, directory="my/project", raise_exception=False)

### DOCKER COMPOSE ENVIRONMENT ###

@patch("src.utils.docker.shutil.copyfile")
@patch("src.utils.docker.os.path.exists", return_value=True)
@patch("src.utils.docker.yaml.safe_load", return_value={'services': {}})
def test_environment_set_service_not_found(_mock_safe_load, _mock_exists, _mock_copyfile):
    with patch("src.utils.docker.Directory.root", return_value="root_dir"):
        with pytest.raises(ValueError) as exc_info:
            Docker.Compose.Environment.set("unknown_service", "VAR", "value")
    assert "Service 'unknown_service' not found." in str(exc_info.value)

@patch("src.utils.docker.os.path.exists", return_value=True)
@patch("src.utils.docker.shutil.copyfile")
@patch("src.utils.docker.yaml.safe_load",
       return_value={'services': {'bike_hivemind': {'environment': []}}})
def test_environment_set_invalid_env_type(_mock_yaml_load, _mock_copyfile, _mock_exists):
    with patch("src.utils.docker.Directory.root", return_value="/mock/root"):
        with pytest.raises(TypeError):
            Docker.Compose.Environment.set("bike_hivemind", "DEFAULT_SPEED", "1000")

@patch("src.utils.docker.os.path.exists", return_value=False)
def test_environment_reset_file_not_found(_mock_exists):
    with patch("src.utils.docker.Directory.root", return_value="/mock/root"):
        with pytest.raises(FileNotFoundError):
            Docker.Compose.Environment.reset(simulation=False)

### DOCKER CONTAINER ###

@patch("src.utils.docker.Command.run")
def test_container_stop_success(mock_run):
    Docker.Container.stop("my_container")
    mock_run.assert_called_once_with(
        ["docker", "stop", "my_container"],
        asynchronous=False,
        raise_exception=False
    )

@patch("src.utils.docker.Command.run", side_effect=Exception("Stop failed"))
def test_container_stop_exception(mock_run):
    with patch("builtins.print") as mock_print:
        Docker.Container.stop("my_container")
        mock_run.assert_called_once_with(
            ["docker", "stop", "my_container"],
            asynchronous=False,
            raise_exception=False
        )
        mock_print.assert_called_once_with("Failed to stop container 'my_container': Stop failed")

@patch("src.utils.docker.Command.run")
def test_container_delete_success(mock_run):
    Docker.Container.delete("my_container")
    mock_run.assert_called_once_with(
        ["docker", "rm", "-f", "my_container"],
        asynchronous=False,
        raise_exception=False
    )

@patch("src.utils.docker.Command.run", side_effect=Exception("Delete failed"))
def test_container_delete_exception(mock_run):
    with patch("builtins.print") as mock_print:
        Docker.Container.delete("my_container")
        mock_run.assert_called_once_with(
            ["docker", "rm", "-f", "my_container"],
            asynchronous=False,
            raise_exception=False
        )
        mock_print.assert_called_once_with(
            "Failed to delete container 'my_container': Delete failed")

### DOCKER NETWORK ###

@patch("src.utils.docker.Command.run")
def test_network_create_success(mock_run):
    Docker.Network.create("my_network")
    mock_run.assert_called_once_with(
        ["docker", "network", "create", "my_network"],
        asynchronous=False,
        raise_exception=False
    )

@patch("src.utils.docker.Command.run", side_effect=Exception("Create failed"))
def test_network_create_exception(mock_run):
    with patch("builtins.print") as mock_print:
        Docker.Network.create("my_network")
        mock_run.assert_called_once_with(
            ["docker", "network", "create", "my_network"],
            asynchronous=False,
            raise_exception=False
        )
        mock_print.assert_called_once_with("Failed to create network 'my_network': Create failed")

@patch.object(Docker.Network, 'delete')
@patch.object(Docker.Network, 'create')
def test_network_recreate(mock_create, mock_delete):
    Docker.Network.recreate("my_network")
    mock_delete.assert_called_once_with("my_network")
    mock_create.assert_called_once_with("my_network")

@patch("src.utils.docker.Command.run")
def test_network_connect_success(mock_run):
    Docker.Network.connect("my_network", "my_container")
    mock_run.assert_called_once_with(
        ["docker", "network", "connect", "my_network", "my_container"],
        asynchronous=False,
        raise_exception=False
    )

@patch("src.utils.docker.Command.run", side_effect=Exception("Connect failed"))
def test_network_connect_exception(mock_run):
    with patch("builtins.print") as mock_print:
        Docker.Network.connect("my_network", "my_container")
        mock_run.assert_called_once_with(
            ["docker", "network", "connect", "my_network", "my_container"],
            asynchronous=False,
            raise_exception=False
        )
        mock_print.assert_called_once_with(
            "Failed to connect container 'my_container' to network "
            "'my_network': Connect failed")

@patch("src.utils.docker.Command.run")
def test_network_delete_success(mock_run):
    Docker.Network.delete("my_network")
    mock_run.assert_called_once_with(
        ["docker", "network", "rm", "my_network"],
        asynchronous=False,
        raise_exception=False
    )

@patch("src.utils.docker.Command.run", side_effect=Exception("Delete failed"))
def test_network_delete_exception(mock_run):
    with patch("builtins.print") as mock_print:
        Docker.Network.delete("my_network")
        mock_run.assert_called_once_with(
            ["docker", "network", "rm", "my_network"],
            asynchronous=False,
            raise_exception=False
        )
        mock_print.assert_called_once_with("Failed to delete network 'my_network': Delete failed")

@patch("src.utils.docker.Command.run")
def test_network_disconnect_success(mock_run):
    Docker.Network.disconnect("my_network", "my_container")
    mock_run.assert_called_once_with(
        ["docker", "network", "disconnect", "my_network", "my_container"],
        asynchronous=False,
        raise_exception=False
    )

@patch("src.utils.docker.Command.run", side_effect=Exception("Disconnect failed"))
def test_network_disconnect_exception(mock_run):
    with patch("builtins.print") as mock_print:
        Docker.Network.disconnect("my_network", "my_container")
        mock_run.assert_called_once_with(
            ["docker", "network", "disconnect", "my_network", "my_container"],
            asynchronous=False,
            raise_exception=False
        )
        mock_print.assert_called_once_with(
            "Failed to disconnect container 'my_container' "
            "from network 'my_network': Disconnect failed")

@patch("src.utils.docker.Command.run")
def test_network_inspect_success(mock_run):
    Docker.Network.inspect("my_network")
    mock_run.assert_called_once_with(
        ["docker", "network", "inspect", "my_network"],
        asynchronous=False,
        raise_exception=False
    )

@patch("src.utils.docker.Command.run", side_effect=Exception("Inspect failed"))
def test_network_inspect_exception(mock_run):
    with patch("builtins.print") as mock_print:
        Docker.Network.inspect("my_network")
        mock_run.assert_called_once_with(
            ["docker", "network", "inspect", "my_network"],
            asynchronous=False,
            raise_exception=False
        )
        mock_print.assert_called_once_with("Failed to inspect network 'my_network': Inspect failed")

@patch("src.utils.docker.Command.run")
def test_network_show_success(mock_run):
    Docker.Network.show()
    mock_run.assert_called_once_with(
        ["docker", "network", "ls"],
        asynchronous=False,
        raise_exception=False
    )

@patch("src.utils.docker.Command.run", side_effect=Exception("Show failed"))
def test_network_show_exception(mock_run):
    with patch("builtins.print") as mock_print:
        Docker.Network.show()
        mock_run.assert_called_once_with(
            ["docker", "network", "ls"],
            asynchronous=False,
            raise_exception=False
        )
        mock_print.assert_called_once_with("Failed to display networks: Show failed")

@patch("src.utils.docker.Command.run")
def test_network_prune_success(mock_run):
    Docker.Network.prune()
    mock_run.assert_called_once_with(
        ["docker", "network", "prune", "-f"],
        asynchronous=False,
        raise_exception=False
    )

@patch("src.utils.docker.Command.run", side_effect=Exception("Prune failed"))
def test_network_prune_exception(mock_run):
    with patch("builtins.print") as mock_print:
        Docker.Network.prune()
        mock_run.assert_called_once_with(
            ["docker", "network", "prune", "-f"],
            asynchronous=False,
            raise_exception=False
        )
        mock_print.assert_called_once_with("Failed to prune unused networks: Prune failed")

### DOCKER DESKTOP ###

@patch("src.utils.docker.Command.run")
def test_docker_desktop_is_running_true(mock_run):
    mock_run.return_value = None
    result = Docker.Desktop.is_running()
    assert result is True
    mock_run.assert_called_once_with(
        ["docker", "info"],
        asynchronous=False,
        kwargs={"verbose": False}
    )

@patch("src.utils.docker.Command.run", side_effect=Exception("Docker not running"))
def test_docker_desktop_is_running_false(mock_run):
    result = Docker.Desktop.is_running()
    assert result is False
    mock_run.assert_called_once_with(
        ["docker", "info"],
        asynchronous=False,
        kwargs={"verbose": False}
    )

@patch("src.utils.docker.Docker.Desktop.is_running", return_value=True)
@patch("src.utils.docker.Command.run")
def test_docker_desktop_start_already_running(mock_run, _mock_is_running):
    Docker.Desktop.start()
    mock_run.assert_not_called()

@patch("src.utils.docker.platform.system", return_value="Windows")
@patch("src.utils.docker.os.path.exists", return_value=True)
@patch("src.utils.docker.Command.run", side_effect=Exception("Start failed"))
@patch("src.utils.docker.Docker.Desktop.is_running", return_value=False)
def test_docker_desktop_start_exception(_mock_is_running, _mock_run, _mock_exists, _mock_platform):
    with patch("builtins.print") as mock_print:
        with pytest.raises(SystemExit) as exc_info:
            Docker.Desktop.start()
        assert exc_info.value.code == 1
        mock_print.assert_any_call("Failed to start the Docker Desktop application: Start failed")

@patch("src.utils.docker.Docker.Desktop.is_running", return_value=True)
def test_docker_desktop_already_running(_mock_is_running):
    with patch("builtins.print") as mock_print:
        Docker.Desktop.start()
        mock_print.assert_called_once_with("Docker Desktop is already running.")

@patch("src.utils.docker.Docker.Desktop.is_running", return_value=False)
@patch("src.utils.docker.platform.system", return_value="Windows")
@patch("src.utils.docker.os.path.exists", return_value=True)
@patch("src.utils.docker.Command.run")
def test_docker_desktop_start_windows(mock_run, _mock_exists, _mock_platform, _mock_is_running):
    with patch("builtins.print") as mock_print:
        Docker.Desktop.start()
        mock_print.assert_any_call("Starting the Docker Desktop application...")
        mock_run.assert_called_once_with(
            [r'C:\Program Files\Docker\Docker\Docker Desktop.exe'],
            asynchronous=False)

@patch("src.utils.docker.Docker.Desktop.is_running", return_value=False)
@patch("src.utils.docker.platform.system", return_value="Linux")
def test_docker_desktop_start_linux(_mock_platform, _mock_is_running):
    with patch("builtins.print") as mock_print:
        Docker.Desktop.start()
        mock_print.assert_any_call("Please start Docker Desktop manually.")

@patch("src.utils.docker.Docker.Desktop.is_running", return_value=False)
@patch("src.utils.docker.platform.system", return_value="Windows")
@patch("src.utils.docker.os.path.exists", return_value=True)
@patch("src.utils.docker.Command.run", side_effect=Exception("Start failed"))
def test_docker_desktop_start_failure(_mock_run, _mock_exists, _mock_platform, _mock_is_running):
    with patch("builtins.print") as mock_print:
        with pytest.raises(SystemExit):
            Docker.Desktop.start()
        mock_print.assert_any_call("Failed to start the Docker Desktop application: Start failed")
