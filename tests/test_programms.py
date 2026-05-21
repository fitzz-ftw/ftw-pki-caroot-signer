
import shlex
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from ftwpki.ca_root_signer.programms import prog_ca_root_singing

# SECTION - Programm: Signing


@pytest.fixture
def ca_test_env(monkeypatch):
    # 1. Pfad zum realen Test-Verzeichnis (relativ zum Projekt-Root)
    # Wir stellen sicher, dass wir den Pfad korrekt auflösen
    project_root = Path(__file__).parent.parent
    testhome_path = project_root / "doc" / "source" / "devel" / "testhome"

    from fitzzftw.devtools.testinfra import TestHomeEnvironment

    env = TestHomeEnvironment(testhome_path)

    # 2. Setup ausführen (bereitet die Verzeichnisse am realen Ort vor)
    env.setup(True)

    # 3. In das Verzeichnis wechseln, das env.setup als CWD vorgesehen hat
    # Meistens ist das der 'testoutput' oder das 'testhome' selbst
    monkeypatch.chdir(env.base_dir)

    # 4. Dateien für den Testlauf bereitstellen
    env.copy2cwd("ca_root_conf.toml")
    Path("privat").mkdir(parents=True, exist_ok=True)
    env.copy2cwd("privat/testpasswd")
    env.copy2cwd("privat/ca.key.pem")
    env.copy2cwd("ca_public/ca.cert", "ca.cert")
    env.copy2cwd("Fitzz-TeXnik-WeltSomewherecity.csr")

    # Automatisierung des Passwort-Prompts
    monkeypatch.setattr("getpass.getpass", lambda _: "strenggeheim")

    # Den Test ausführen lassen
    yield env

    # 5. Aufräumen nach dem Test
    env.clean_home()
    env.teardown()

@pytest.mark.skipif(
    sys.platform == "win32", reason="Windows handles file locks differently (PermissionError in CI)"
)
def test_prog_ca_root_singing_success(ca_test_env):
    """Szenario: Alles korrekt -> Return 0"""
    cmd = (
        "--conf-file ca_root_conf.toml -k privat/ca "
        "--private-dir privat --policy-name intermediate "
        "-c ca.cert testpasswd Fitzz-TeXnik-WeltSomewherecity.csr"
    )

    argv = shlex.split(cmd)

    result = prog_ca_root_singing(argv)

    assert result == 0
    # Check ob das Zertifikat erstellt wurde
    assert Path("Fitzz-TeXnik-WeltSomewherecity.crt.pem").exists()
    # Check ob Datenbank-Eintrag existiert
    assert Path("db/index.txt").exists()

@pytest.mark.skipif(
    sys.platform == "win32", reason="Windows handles file locks differently (PermissionError in CI)"
)
def test_prog_ca_root_singing_success_dbdir_exists(ca_test_env):
    """Szenario: Alles korrekt -> Return 0"""
    cmd = (
        "--conf-file ca_root_conf.toml -k privat/ca "
        "--private-dir privat --policy-name intermediate "
        "-c ca.cert testpasswd Fitzz-TeXnik-WeltSomewherecity.csr"
    )

    argv = shlex.split(cmd)
    # NEU: Das db-Verzeichnis manuell vorab anlegen,
    # um den Branch in Zeile 110 zu covern.
    Path("db").mkdir(parents=True, exist_ok=True)

    result = prog_ca_root_singing(argv)

    assert result == 0
    # Check ob das Zertifikat erstellt wurde
    assert Path("Fitzz-TeXnik-WeltSomewherecity.crt.pem").exists()
    # Check ob Datenbank-Eintrag existiert
    assert Path("db/index.txt").exists()

@pytest.mark.skipif(
    sys.platform == "win32", reason="Windows handles file locks differently (PermissionError in CI)"
)
def test_prog_ca_root_singing_validation_fail(ca_test_env):
    """Szenario: Policy-Verstoß (falsche DN) -> Return 1"""
    # Hier müsstest du ein CSR nutzen, das die Policy verletzt
    # Oder die Policy in der TOML kurzfristig via Code manipulieren
    # Beispiel: Wir setzen eine Policy, die 'Match' verlangt, aber das CSR hat andere Daten

    # (Simulierter fehlerhafter Aufruf oder manipulierte Config)
    # ... Logik für Return 1 ...

    with pytest.MonkeyPatch().context() as m:
        m.setattr("getpass.getpass", lambda _: "strenggeheim")

        cmd = (
            "--conf-file ca_root_conf.toml -k privat/ca "
            "--private-dir privat -c ca.cert testpasswd "
            "Fitzz-TeXnik-WeltSomewherecity.csr"
        )

        result = prog_ca_root_singing(shlex.split(cmd))
        assert result == 1


VALID_ARGV = ["my_pass_file", "my_request.csr"]

@pytest.mark.skipif(
    sys.platform == "win32", reason="Windows handles file locks differently (PermissionError in CI)"
)
def test_prog_ca_root_singing_exception():
    # Testet den harten Absturz (Return 2)
    with patch("ftwpki.ca_root_signer.programms.CSRSigningParser") as mock_parser:
        # Wir lassen die Instanziierung des Parsers scheitern
        mock_parser.side_effect = Exception("Crash")

        result = prog_ca_root_singing(VALID_ARGV)
        assert result == 2


# !SECTION Programm: Signing
