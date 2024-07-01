import pytest

all_users = ("login,password", [("standard_user", "secret_sauce"),
                                pytest.param("locked_out_user", "secret_sauce",
                                             marks=pytest.mark.xfail(reason="пользователь заблокирован")),
                                ("problem_user", "secret_sauce"),
                                ("performance_glitch_user", "secret_sauce"),
                                ("error_user", "secret_sauce"),
                                ("visual_user", "secret_sauce")])  # данные всех пользователей

standard_user = ("login,password", [("standard_user", "secret_sauce")])
problem_user = ("login,password", [("problem_user", "secret_sauce")])
locked_out_user = ("login,password", [("locked_out_user", "secret_sauce")])
non_existent_user = ("login,password", [("user", "user")])
empty_login = ("login,password", [("", "secret_sauce")])
empty_password = ("login,password", [("standard_user", "")])

