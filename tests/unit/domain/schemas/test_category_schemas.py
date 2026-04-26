from datetime import datetime
from uuid import UUID

import pytest
from pydantic import ValidationError

from api.schemas.category import CategoryCreate, CategoryResponse


class TestCategoryCreateSchema:
    def test_create_with_required_fields_only(self) -> None:
        schema = CategoryCreate(name="Hardware Support")
        assert schema.name == "Hardware Support"
        assert schema.description is None

    def test_create_with_all_fields(self) -> None:
        schema = CategoryCreate(
            name="Software Support", description="For software related issues"
        )
        assert schema.name == "Software Support"
        assert schema.description == "For software related issues"

    def test_create_validates_name_min_length(self) -> None:
        with pytest.raises(ValidationError):
            CategoryCreate(name="")

    def test_create_validates_name_max_length(self) -> None:
        long_name = "a" * 101
        with pytest.raises(ValidationError):
            CategoryCreate(name=long_name)

    def test_create_validates_description_max_length(self) -> None:
        long_description = "a" * 501
        with pytest.raises(ValidationError):
            CategoryCreate(name="Valid Name", description=long_description)


class TestCategoryResponseSchema:
    def test_response_with_all_fields(self) -> None:
        category_id = UUID("12345678-1234-5678-1234-567812345678")
        created_date = datetime(2024, 1, 1, 12, 0, 0)

        schema = CategoryResponse(
            id=category_id,
            name="Network Support",
            description="For network issues",
            created_at=created_date,
        )

        assert schema.id == category_id
        assert schema.name == "Network Support"
        assert schema.description == "For network issues"
        assert schema.created_at == created_date

    def test_response_with_null_description(self) -> None:
        category_id = UUID("12345678-1234-5678-1234-567812345678")
        created_date = datetime(2024, 1, 1, 12, 0, 0)

        schema = CategoryResponse(
            id=category_id, name="Printer Support", description=None, created_at=created_date
        )

        assert schema.id == category_id
        assert schema.name == "Printer Support"
        assert schema.description is None
        assert schema.created_at == created_date
