from cargo_workspace import Workspace, Version, Crate

def test_package_metadata_works():
    content = """
    [package]
    name = "test"
    [package.metadata.docs.rs]
    targets = ["x86_64-unknown-linux-gnu"]
    custom = "value"
    """
    crate = Crate.from_raw_manifest(content, "path")
    assert crate.metadata.get('docs.rs.targets') == ["x86_64-unknown-linux-gnu"]

    content = """
    [package]
    name = "test"
    [package.metadata.polkadot-sdk]
    internal = true
    """
    crate = Crate.from_raw_manifest(content, "path")
    assert crate.metadata.get("polkadot-sdk.internal")

def test_version_from_str():
    assert Version.from_str("0.1.2") == Version(0, 1, 2)
    assert Version.from_str("0.1.2-alpha") == Version(0, 1, 2, "alpha")
    assert Version.from_str("0.1.2-beta.123") == Version(0, 1, 2, "beta.123")
    assert Version.from_str("0.1.2-beta-123") == Version(0, 1, 2, "beta-123")

def test_parse_sdk():
    w = Workspace.from_path("../polkadot-sdk/Cargo.toml")
    assert w.path == "../polkadot-sdk"
    assert w.find_stray_manifests() == [
        '../polkadot-sdk/substrate/frame/contracts/fixtures/build/Cargo.toml',
        '../polkadot-sdk/substrate/frame/contracts/fixtures/contracts/common/Cargo.toml'
    ]

    crates = w.crates
    assert len(crates) >= 400
    assert crates[0].name == "bridge-runtime-common"
    assert crates[0].path == "../polkadot-sdk/bridges/bin/runtime-common/Cargo.toml"
    assert crates[0].version == Version(0, 7)
    assert crates[0].version.suffix is None
    assert crates[0].publish

def test_semver_str_works():
    assert str(Version(0)) == "0.0.0"
    assert str(Version(0, 0)) == "0.0.0"
    assert str(Version(0, 0, 0)) == "0.0.0"

    assert str(Version(1)) == "1.0.0"
    assert str(Version(1, 0)) == "1.0.0"
    assert str(Version(1, 0, 0)) == "1.0.0"
    assert str(Version(0, 1)) == "0.1.0"
    assert str(Version(0, 1, 0)) == "0.1.0"
    assert str(Version(0, 0, 1)) == "0.0.1"

    assert str(Version(1, 2, 3)) == "1.2.3"

def test_semver_str_suffix_works():
    assert str(Version(0, 0, 0, "suff.123")) == "0.0.0-suff.123"
    assert str(Version(0, 1, 0, "suff.123")) == "0.1.0-suff.123"
    assert str(Version(0, 0, 1, "suff-123")) == "0.0.1-suff-123"

def test_semver_major_works():
    assert Version(1).cargo_convention().major == 1
    assert Version(0, 1).cargo_convention().major == 1
    assert Version(0, 0, 1).cargo_convention().major == 1

    assert Version(1).cargo_convention().major == 1
    assert Version(0, 1).cargo_convention().major == 1
    assert Version(0, 0, 1).cargo_convention().major == 1

    assert Version(1).x == 1
    assert Version(0, 1).y == 1
    assert Version(0, 0, 1).z == 1

def test_semver_minor_works():
    assert Version(1).cargo_convention().minor == 0
    assert Version(1, 2).cargo_convention().minor == 2

    assert Version(0, 1).cargo_convention().minor == 0
    assert Version(0, 1, 2).cargo_convention().minor == 2

    assert Version(0, 1).cargo_convention().minor == 0
    assert Version(0, 1, 2).cargo_convention().minor == 2

    assert Version(0, 0, 1).cargo_convention().minor == None

def test_semver_patch_works():
    assert Version(1).cargo_convention().patch == 0
    assert Version(1, 2).cargo_convention().patch == 0
    assert Version(1, 2, 3).cargo_convention().patch == 3

    assert Version(0, 1).cargo_convention().patch == None
    assert Version(0, 1, 2).cargo_convention().patch == None

    assert Version(0, 0, 1).cargo_convention().patch == None

def test_semver_same_diff_works():
    v1 = Version(1, 2, 3).cargo_convention()
    v2 = Version(1, 2, 3).cargo_convention()

    assert v1.diff(v2).is_stable()
    assert not v1.diff(v2).is_patch()
    assert not v1.diff(v2).is_minor()
    assert not v1.diff(v2).is_major()

def test_semver_diff_works():
    v1 = Version(1, 2, 3).cargo_convention()
    v2 = Version(1, 2, 4).cargo_convention()
    assert v1.diff(v2).is_patch()
    assert v1.diff(v2).is_stable()

    v1 = Version(1, 2, 3).cargo_convention()
    v2 = Version(1, 3, 4).cargo_convention()
    assert v1.diff(v2).is_minor()
    assert not v1.diff(v2).is_patch()
    assert v1.diff(v2).is_stable()

    v1 = Version(1, 2, 3).cargo_convention()
    v2 = Version(2, 3, 4).cargo_convention()
    assert v1.diff(v2).is_major()
    assert not v1.diff(v2).is_minor()
    assert not v1.diff(v2).is_patch()
    assert v1.diff(v2).is_stable()

    v1 = Version(1, 2, 3).cargo_convention()
    v2 = Version(1, 2, 3).cargo_convention()
    assert not v1.diff(v2).is_patch()
    assert not v1.diff(v2).is_minor()
    assert not v1.diff(v2).is_major()
    assert v1.diff(v2).is_stable()

def test_semver_strict_diff_works():
    v1 = Version(1, 2, 3).cargo_convention()
    v2 = Version(1, 3, 4).cargo_convention()
    assert v1.diff(v2).is_minor()
    assert not v1.diff(v2).is_patch()
    assert not v1.diff(v2).is_strict_minor()

def test_semver_unstable_diff_works():
    v1 = Version(0, 2, 3).cargo_convention()
    v2 = Version(0, 2, 4).cargo_convention()
    assert v1.diff(v2).is_minor()
    assert not v1.diff(v2).is_stable()

    v1 = Version(0, 0, 3).cargo_convention()
    v2 = Version(0, 0, 4).cargo_convention()
    assert v1.diff(v2).is_major()
    assert not v1.diff(v2).is_stable()
    
    v1 = Version(1, 0, 0, "alpha").cargo_convention()
    v2 = Version(1, 0, 1, "alpha").cargo_convention()
    assert v1.diff(v2).is_patch()
    assert not v1.diff(v2).is_stable()

def test_semver_suffix_diff_works():
    v1 = Version(1, 2, 3, "alpha").cargo_convention()
    v2 = Version(1, 2, 3, "beta").cargo_convention()
    assert not v1.diff(v2).is_patch()
    assert not v1.diff(v2).is_minor()
    assert not v1.diff(v2).is_major()
    assert not v1.diff(v2).is_stable()
    assert not v1.diff(v2).is_empty()
