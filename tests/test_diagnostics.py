"""ROCm version detection and the numba-hip install advice. No GPU needed."""

from harmonize import diagnostics


def test_rocm_version_from_version_file(tmp_path):
    rocm = tmp_path / "rocm"
    (rocm / ".info").mkdir(parents=True)
    (rocm / ".info" / "version").write_text("7.2.1-81\n")
    assert diagnostics.detect_rocm_version(str(rocm)) == (7, 2, 1)


def test_rocm_version_from_directory_name(tmp_path):
    rocm = tmp_path / "rocm-6.4.0"
    rocm.mkdir()
    assert diagnostics.detect_rocm_version(str(rocm)) == (6, 4, 0)


def test_rocm_version_falls_back_to_hipconfig(tmp_path, monkeypatch):
    # hipconfig reports HIP's version: only its major and minor match ROCm's
    monkeypatch.setattr(diagnostics, "run_text", lambda command: "7.2.53211-abc")
    rocm = tmp_path / "rocm"
    rocm.mkdir()
    assert diagnostics.detect_rocm_version(str(rocm)) == (7, 2)


def test_hint_for_a_release_the_repository_builds():
    hint = diagnostics.numba_hip_install_hint((7, 2, 1))
    assert '"numba-hip[rocm-7-2-1] @ git+https://github.com/ROCm/numba-hip.git"' in hint
    assert "pip install numba-hip " not in hint


def test_hint_for_a_newer_release():
    hint = diagnostics.numba_hip_install_hint((7, 3, 0))
    assert "pip install numba-hip " in hint
    assert "git+" not in hint


def test_hint_without_a_full_version():
    for version in (None, (7, 2)):
        hint = diagnostics.numba_hip_install_hint(version)
        assert "rocm-X-Y-Z" in hint and "pip install numba-hip " in hint
