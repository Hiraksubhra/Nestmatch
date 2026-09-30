import os
import uuid
from typing import Optional, Dict
from fastapi import UploadFile
from app.core.config import settings


class PhotoService:
    @staticmethod
    async def upload_image(file: UploadFile, folder: str = "listings") -> Dict[str, str]:
        """
        Uploads image to Cloudinary if credentials are provided,
        otherwise falls back to storing in local static uploads directory.
        """
        filename = f"{uuid.uuid4()}_{file.filename}"
        contents = await file.read()

        is_real_cloudinary = (
            settings.CLOUDINARY_CLOUD_NAME
            and settings.CLOUDINARY_API_KEY
            and settings.CLOUDINARY_API_SECRET
            and "your_cloudinary" not in settings.CLOUDINARY_CLOUD_NAME
        )

        if is_real_cloudinary:
            try:
                import cloudinary
                import cloudinary.uploader

                cloudinary.config(
                    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
                    api_key=settings.CLOUDINARY_API_KEY,
                    api_secret=settings.CLOUDINARY_API_SECRET,
                    secure=True,
                )
                upload_result = cloudinary.uploader.upload(
                    contents,
                    folder=f"nestmatch/{folder}",
                    resource_type="image",
                )
                return {
                    "url": upload_result.get("secure_url", upload_result.get("url")),
                    "public_id": upload_result.get("public_id"),
                }
            except Exception as e:
                # If Cloudinary upload fails, fallback to local storage
                print(f"Cloudinary upload failed, falling back: {e}")

        # Local fallback
        upload_dir = os.path.join(os.getcwd(), "static", "uploads", folder)
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, filename)

        with open(file_path, "wb") as f:
            f.write(contents)

        local_url = f"/static/uploads/{folder}/{filename}"
        return {
            "url": local_url,
            "public_id": filename,
        }

    @staticmethod
    async def delete_image(public_id: str) -> None:
        if settings.CLOUDINARY_CLOUD_NAME and settings.CLOUDINARY_API_KEY and settings.CLOUDINARY_API_SECRET:
            try:
                import cloudinary
                import cloudinary.uploader
                cloudinary.uploader.destroy(public_id)
            except Exception as e:
                print(f"Cloudinary delete failed: {e}")
