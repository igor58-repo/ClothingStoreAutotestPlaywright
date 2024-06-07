import pytest

all_users = ("login,password", [("standard_user", "secret_sauce"),
                                pytest.param("locked_out_user", "secret_sauce",
                                             marks=pytest.mark.xfail(reason='пользователь заблокирован')),
                                ("problem_user", "secret_sauce"),
                                ("performance_glitch_user", "secret_sauce"),
                                ("error_user", "secret_sauce"),
                                ("visual_user", "secret_sauce")])  # данные всех пользователей

standard_user = ("login,password", [("standard_user", "secret_sauce")])
