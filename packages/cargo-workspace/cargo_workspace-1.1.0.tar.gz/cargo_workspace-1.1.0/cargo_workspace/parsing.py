import os
import tomllib

class Version:
	def __init__(self, x, y=0, z=0, suffix=None):
		self._x = x
		self._y = y
		self._z = z
		self._suffix = suffix
	
	def __str__(self):
		su = f"-{self._suffix}" if self._suffix is not None else ""

		return f"{self._x}.{self._y}.{self._z}{su}"
	
	def __eq__(self, other):
		return (self._x == other._x) and (self._y == other._y) and (self._z == other._z) and (self._suffix == other._suffix)

	def from_str(s):
		if '-' in s:
			splits = s.partition('-')
			ver = splits[0]
			suffix = splits[2]
		else:
			ver = s
			suffix = None

		v = Version.from_str_no_suffix(ver)
		v._suffix = suffix
		
		return v
	
	def from_str_no_suffix(s):
		parts = s.split('.')
		if len(parts) == 1:
			return Version(int(parts[0]))
		if len(parts) == 2:
			return Version(int(parts[0]), int(parts[1]))
		if len(parts) == 3:
			return Version(int(parts[0]), int(parts[1]), int(parts[2]))
		raise ValueError(f'Invalid version string: {s}')
	
	def cargo_convention(self):
		return CargoVersion(self)
	
	def is_stable(self):
		return self._suffix is None and self._x > 0
	
	def __getattr__(self, name):
		if name == 'x':
			return self._x
		if name == 'y':
			return self._y
		if name == 'z':
			return self._z
		if name == 'suffix':
			return self._suffix
		
		raise AttributeError(f'No such attribute: {name}')
class CargoVersion:
	def __init__(self, version):
		self._version = version
	
	def __eq__(self, other):
		return self._version == other._version

	def __str__(self):
		return str(self._version)

	def is_stable(self):
		return self._version.is_stable()

	def diff(self, other):
		return CargoVersionBump(self, other)

	def __getattr__(self, name):
		if name == 'major':
			return self._major()
		if name == 'minor':
			return self._minor()
		if name == 'patch':
			return self._patch()
		if name == 'suffix':
			return self._suffix()
		
		raise AttributeError(f'No such attribute: {name}')

	def _major(self):
		if self._version.x > 0:
			return self._version.x
		if self._version.y > 0:
			return self._version.y
		return self._version.z
	
	def _minor(self):
		if self._version.x > 0:
			return self._version.y
		if self._version.y > 0:
			return self._version.z
		return None
	
	def _patch(self):
		if self._version.x > 0:
			return self._version.z
		return None
	
	def _suffix(self):
		return self._version.suffix()

class CargoVersionBump:
	def __init__(self, old, new):
		self._old = old
		self._new = new
	
	def is_stable(self):
		return self._old.is_stable() and self._new.is_stable()
	
	def is_empty(self):
		return self._old == self._new
	
	def is_major(self):
		return self._old.major != self._new.major
	
	def is_strict_major(self):
		return self.is_major() and (self._old.minor == 0) and (self._old.patch == 0)
	
	def is_minor(self):
		return (self._old.major == self._new.major) and (self._old.minor != self._new.minor)
	
	def is_strict_minor(self):
		return self.is_minor() and (self._old.patch == 0)
	
	def is_patch(self):
		return (self._old.major == self._new.major) and (self._old.minor == self._new.minor) and (self._old.patch != self._new.patch)

class Crate:
	def __init__(self, manifest, path):
		self._manifest = manifest
		self._path = path

	def from_path(path):
		# check if the file exists
		if not os.path.exists(path):
			raise ValueError(f'Could not load crate manifest at {path}')

		try:
			with open(path, 'r') as f:
				content = f.read()
				return Crate.from_raw_manifest(content, path)
		except FileNotFoundError:
			raise ValueError(f'Could not load crate manifest at {path}')
	
	def from_raw_manifest(content, path):
		manifest = tomllib.loads(content)
		
		return Crate(manifest, path)

	def is_crate_manifest(manifest):
		if 'workspace' in manifest:
			return ValueError(f'A single crate was expected at {path}, but it does contain a workspace section')
		if not 'package' in manifest:
			return ValueError(f'Could not find package in crate manifest at {path}')

	def __getattr__(self, name):
		# Not using 'match' here since it requires python version 3.10.
		if name == 'name':
			return self._crate()['name']
		if name == 'version':
			return self._get_version()
		if name == 'path':
			return self._path
		if name == 'metadata':
			return self._get_metadata()
		if name == 'publish':
			return self._get_publish()

		raise AttributeError(f'No such attribute: {name}')

	def _get_version(self):
		if not 'version' in self._crate():
			raise ValueError(f'Could not find version in crate manifest at {self._path}')
		return Version.from_str(self._crate()['version'])

	def _get_metadata(self):
		return Metadata(self._crate().get('metadata', {}))

	def _crate(self):
		if not 'package' in self._manifest:
			raise ValueError(f'Could not find package in crate manifest at {self._path}')
		return self._manifest['package']		
	
	def _get_publish(self):
		if not 'publish' in self._crate():
			return True

		return bool(self._crate()['publish'])

class Manifest:
	def __init__(self, content, path):
		self._content = content
		self._path = path
	
	def from_path(path):
		with open(path, 'rb') as f:
			manifest = tomllib.load(f)
		return Manifest(manifest, path)
	
	def into_crate(self, path):
		return Crate(self._content, path)

class Metadata:
	'''
	A typed wrapper around a dictionary that represents the metadata section of a crate manifest.
	'''

	def __init__(self, content):
		self._content = content
	
	def get(self, key, default=None):
		splits = key.split('.')
		obj = self._content
		
		for split in splits:
			if split in obj:
				obj = obj[split]
			else:
				return default
		return obj

class Workspace:
	def __init__(self, manifest, root_path=None):
		self._manifest = manifest
		self._root_dir = root_path or os.getcwd()
		self._crates = Workspace.__crates_from_manifest(manifest, self._root_dir)

	def from_raw_manifest(content):
		manifest = tomllib.loads(content)
		return Workspace(manifest)		

	def from_path(path, allow_dir=True):
		if not path.endswith('Cargo.toml') and allow_dir:
			path = os.path.join(path, 'Cargo.toml')
		
		try:
			with open(path, 'rb') as f:
				manifest = tomllib.load(f)
		except FileNotFoundError:
			raise ValueError(f'Could not load workspace manifest at {path}')
		
		root_dir = os.path.dirname(path)
		return Workspace(manifest, root_dir)

	def __crates_from_manifest(manifest, root_dir):
		crates = []

		if 'workspace' not in manifest or 'members' not in manifest['workspace']:
			return		

		# Go through the list of members and create Crate objects:
		for path in manifest['workspace']['members']:
			path = os.path.join(root_dir, path)
			path = os.path.join(path, 'Cargo.toml')

			crate = Crate.from_path(path)
			crates.append(crate)
		
		Workspace.__check_no_duplicate_paths(crates)
		return crates
	
	def __check_no_duplicate_paths(crates):
		paths = set()
		for crate in crates:
			path = os.path.abspath(crate.path)
			if path in paths:
				raise ValueError(f'There are two crates with the same absolute path {path}')

			paths.add(path)

	def ensure_no_stray_manifests(self):
		stray = self.find_stray_manifests()

		if stray is not None:
			raise ValueError(f'Found stray manifest(s) at: {stray}')
	
	def find_stray_manifests(self, excluded_crates=None):
		all_paths = Workspace.find_manifest_paths(self._root_dir, exclude_dirs=["target"])
		workspace_paths = [os.path.abspath(crate.path) for crate in self.crates]
		stray_paths = []

		for path in all_paths:
			if os.path.abspath(path) not in workspace_paths:
				stray_paths.append(path)
		
		stray_paths.remove(os.path.join(self._root_dir, 'Cargo.toml'))
		stray_paths.sort()

		if len(stray_paths) > 0:
			return stray_paths
		return None
	
	def find_manifest_paths(root_dir, exclude_dirs):
		paths = []
		for root, dirs, files in os.walk(root_dir):
			if any(exclude in root for exclude in exclude_dirs):
				continue
			if 'Cargo.toml' in files:
				path = os.path.join(root, 'Cargo.toml')

				if os.path.islink(path):
					raise ValueError(f'Found symlinked manifest at {path}')

				paths.append(path)

		paths.sort()
		return paths
	
	def __getattr__(self, name):
		if name == 'path':
			return self._root_dir
		if name == 'crates':
			return self._crates

		raise AttributeError(f'No such attribute: {name}')

	def crate_by_name(self, name):
		found = []
		for crate in self.crates():
			if crate.name() == name:
				found.append(crate)
		
		if len(found) > 1:
			raise ValueError(f'Found multiple crates with name {name}')
		if len(found) == 0:
			return None
		return found[0]
		
