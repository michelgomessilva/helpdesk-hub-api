from uuid import UUID

from domain.entities import Category
from infrastructure.repositories import InMemoryCategoryRepository


def test_save_assigns_uuid_id() -> None:
    repo = InMemoryCategoryRepository()
    category = Category(name="Hardware Support", description="Hardware issues")

    saved_category = repo.save(category)

    assert isinstance(saved_category.id, UUID)
    assert str(saved_category.id) != ""


def test_save_assigns_created_at() -> None:
    repo = InMemoryCategoryRepository()
    category = Category(name="Software Support", description="Software issues")

    saved_category = repo.save(category)

    assert saved_category.created_at is not None


def test_save_two_categories_have_different_ids() -> None:
    repo = InMemoryCategoryRepository()
    category1 = Category(name="Network Support", description="Network issues")
    category2 = Category(name="Printer Support", description="Printer issues")

    saved_category1 = repo.save(category1)
    saved_category2 = repo.save(category2)

    assert saved_category1.id != saved_category2.id


def test_save_preserves_name_and_description() -> None:
    repo = InMemoryCategoryRepository()
    category = Category(name="Database Support", description="Database issues")

    saved_category = repo.save(category)

    assert saved_category.name == "Database Support"
    assert saved_category.description == "Database issues"


def test_list_all_returns_empty_on_new_repository() -> None:
    repo = InMemoryCategoryRepository()

    categories = repo.list_all()

    assert categories == []


def test_list_all_returns_all_saved_categories() -> None:
    repo = InMemoryCategoryRepository()
    category1 = Category(name="Hardware Support", description="Hardware issues")
    category2 = Category(name="Software Support", description="Software issues")

    repo.save(category1)
    repo.save(category2)
    categories = repo.list_all()

    assert len(categories) == 2
    assert categories[0].name == "Hardware Support"
    assert categories[1].name == "Software Support"
    assert categories[0].description == "Hardware issues"
    assert categories[1].description == "Software issues"


def test_repositories_have_independent_stores() -> None:
    repo1 = InMemoryCategoryRepository()
    repo2 = InMemoryCategoryRepository()

    category1_r1 = Category(name="Category 1", description="Repo 1")
    category1_r2 = Category(name="Category 2", description="Repo 2")

    repo1.save(category1_r1)
    repo2.save(category1_r2)

    assert len(repo1.list_all()) == 1
    assert len(repo2.list_all()) == 1
    assert repo1.list_all()[0].name == "Category 1"
    assert repo2.list_all()[0].name == "Category 2"
