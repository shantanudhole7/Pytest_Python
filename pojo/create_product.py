import mimetypes
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class CreateProduct:
    productName: str = "Cotton T-shirt"
    productAddedBy: str = "644d13ca568c3e9fb15feee3"
    productCategory: str = "fashion"
    productSubCategory: str = "T-Shirt"
    productPrice: str = "11500"
    productDescription: str = "Test"
    productFor: str = "Men"
    productImage: str = "data/files/T-Shirt.png"

    def to_dict(self) -> dict:
        return asdict(self)

    def to_multipart(self) -> dict:
        """Text fields as form fields, productImage as a file part."""
        data = self.to_dict()
        image = Path(data.pop("productImage"))
        data["productImage"] = {
            "name": image.name,
            "mimeType": mimetypes.guess_type(image.name)[0] or "application/octet-stream",
            "buffer": image.read_bytes(),
        }
        return data
