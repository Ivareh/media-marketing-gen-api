from typing import Any


class BaseTest:
    """Base testing class for testing API and CRUD operations"""

    num_initial_objs = 0  # If some models have objs in db before tests start

    def partial_fields_comparison(
        self, obj: dict[str, Any], compare_obj: dict[str, Any]
    ) -> None:
        """
        Assert equality for shared fields between two dicts

        Ignores fields only existing to one dict
        """

        common_fields = obj.keys() & compare_obj.keys()
        for field in common_fields:
            assert str(obj[field]) == str(
                compare_obj[field]
            ), f"Mismatch in field '{field}'"
