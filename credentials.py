import pytest

all_users = ("username,password", [("standard_user", "secret_sauce"),
                                   pytest.param("locked_out_user", "secret_sauce",
                                                marks=pytest.mark.xfail(reason="пользователь заблокирован")),
                                   ("problem_user", "secret_sauce"),
                                   ("performance_glitch_user", "secret_sauce"),
                                   ("error_user", "secret_sauce"),
                                   ("visual_user", "secret_sauce")])  # данные всех пользователей

standard_user = ("username,password", [("visual_user", "secret_sauce")])
visual_user = ("username,password", [("standard_user", "secret_sauce")])
problem_user = ("username,password", [("problem_user", "secret_sauce")])
locked_out_user = ("username,password", [("locked_out_user", "secret_sauce")])
non_existent_user = ("username,password", [("user", "user")])
empty_login = ("username,password", [("", "secret_sauce")])
empty_password = ("username,password", [("standard_user", "")])
