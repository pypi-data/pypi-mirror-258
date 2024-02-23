import unreal
import yaml

class Common():
    def __init__(self, name: str) -> None:
        self.name=name

    def load_config_file(file_path: str) -> None:
        with open(file_path, 'r') as file:
            config_data = yaml.safe_load(file)

        return config_data

    def create_static_mesh_from_asset(asset_path: str) -> None:
        # Specify the path to the asset
        asset_path = asset_path

        # Load the asset
        asset = unreal.EditorAssetLibrary().load_asset(asset_path)

        # Create the static mesh and output if successful
        if asset:
            static_mesh = unreal.EditorStaticMeshLibrary.create_static_mesh(asset)
            if static_mesh:
                unreal.log_warning("Static Mesh created successfully!")
            else:
                unreal.log_warning("Failed to create Static Mesh.")
        else:
            unreal.log_warning("Failed to load asset from path: " + asset_path)