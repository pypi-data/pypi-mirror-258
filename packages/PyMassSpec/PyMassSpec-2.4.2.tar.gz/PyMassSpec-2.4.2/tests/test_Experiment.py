#############################################################################
#                                                                           #
#    PyMassSpec software for processing of mass-spectrometry data           #
#    Copyright (C) 2019-2020 Dominic Davis-Foster                           #
#                                                                           #
#    This program is free software; you can redistribute it and/or modify   #
#    it under the terms of the GNU General Public License version 2 as      #
#    published by the Free Software Foundation.                             #
#                                                                           #
#    This program is distributed in the hope that it will be useful,        #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#    GNU General Public License for more details.                           #
#                                                                           #
#    You should have received a copy of the GNU General Public License      #
#    along with this program; if not, write to the Free Software            #
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.              #
#                                                                           #
#############################################################################

# stdlib
from typing import List

# 3rd party
import pytest
from domdf_python_tools.paths import PathPlus

# this package
from pyms.Experiment import Experiment, load_expr, read_expr_list
from pyms.Peak.Class import Peak
from pyms.Utils.Utils import is_sequence_of

# this package
from .constants import *


def test_Experiment(expr: Experiment, filtered_peak_list: List[Peak]):
	assert isinstance(expr, Experiment)
	# Errors
	for obj in [*test_numbers, test_dict, *test_lists]:
		with pytest.raises(TypeError):
			Experiment(obj, filtered_peak_list)  # type: ignore[arg-type]

	for obj in [test_string, test_int, test_dict, *test_lists]:
		with pytest.raises(TypeError):
			Experiment(test_string, obj)  # type: ignore[arg-type]


def test_equality(expr: Experiment):
	assert expr == Experiment(expr.expr_code, expr.peak_list)
	assert expr != Experiment(test_string, expr.peak_list)
	assert expr != test_float
	assert expr != test_int
	assert expr != test_string
	assert expr != test_list_ints
	assert expr != test_list_strs
	assert expr != test_dict
	assert expr != test_tuple


def test_len(expr: Experiment):
	assert len(expr) == 641


def test_expr_code(expr: Experiment):
	assert isinstance(expr.expr_code, str)
	assert expr.expr_code == "ELEY_1_SUBTRACT"


def test_peak_list(expr: Experiment, filtered_peak_list: List[Peak]):
	assert isinstance(expr.peak_list, list)
	assert is_sequence_of(filtered_peak_list, Peak)
	assert expr.peak_list == filtered_peak_list


def test_sele_rt_range(expr: Experiment, filtered_peak_list: List[Peak]):
	expr.sele_rt_range(["6.5m", "21m"])
	assert expr.peak_list != filtered_peak_list

	for obj in [test_string, *test_numbers, test_dict]:
		with pytest.raises(TypeError):
			expr.sele_rt_range(obj)  # type: ignore[arg-type]

	for obj in test_lists:
		with pytest.raises(ValueError, match="'rt_range' must have exactly two elements"):
			expr.sele_rt_range(obj)  # type: ignore[arg-type]


@pytest.fixture()
def expr_filename(expr: Experiment, tmp_pathplus: PathPlus) -> PathPlus:
	filename = tmp_pathplus / "ELEY_1_SUBTRACT.expr"
	expr.dump(filename)
	return filename


def test_dump_errors(expr: Experiment):
	for obj in [*test_numbers, test_dict, *test_lists]:
		with pytest.raises(TypeError):
			expr.dump(obj)  # type: ignore[arg-type]


def test_load_expr(filtered_peak_list: List[Peak], pyms_datadir: PathPlus, expr_filename: PathPlus):
	expr = load_expr(expr_filename)
	assert isinstance(expr, Experiment)

	assert isinstance(expr.expr_code, str)
	assert expr.expr_code == "ELEY_1_SUBTRACT"

	assert isinstance(expr.peak_list, list)
	assert is_sequence_of(expr.peak_list, Peak)

	assert expr.peak_list == filtered_peak_list
	expr.sele_rt_range(["6.5m", "21m"])

	# Errors
	for obj in [*test_numbers, test_dict, *test_lists]:
		with pytest.raises(TypeError):
			load_expr(obj)  # type: ignore[arg-type]

	with pytest.raises(FileNotFoundError, match="No such file or directory: .*non-existent.expr.*"):
		load_expr(pyms_datadir / "non-existent.expr")
	with pytest.raises(TypeError, match="The loaded file is not an experiment file"):
		load_expr(pyms_datadir / "not-an-experiment.expr")


def test_read_expr_list(filtered_peak_list: List[Peak], expr_filename: PathPlus, tmp_pathplus: PathPlus):
	(tmp_pathplus / "read_expr_list.txt").write_lines([str(expr_filename)] * 5)
	expr_list = read_expr_list(tmp_pathplus / "read_expr_list.txt")
	assert isinstance(expr_list, list)
	assert is_sequence_of(expr_list, Experiment)

	expr = expr_list[0]
	assert isinstance(expr.expr_code, str)
	assert expr.expr_code == "ELEY_1_SUBTRACT"

	assert isinstance(expr.peak_list, list)
	assert is_sequence_of(expr.peak_list, Peak)
	assert expr.peak_list == filtered_peak_list

	expr.sele_rt_range(["6.5m", "21m"])

	# Errors
	for obj in [*test_numbers, test_dict, *test_lists]:
		with pytest.raises(TypeError):
			read_expr_list(obj)  # type: ignore[arg-type]

	with pytest.raises(FileNotFoundError, match="No such file or directory: .*non-existent.expr.*"):
		read_expr_list("non-existent.expr")
	with pytest.raises(FileNotFoundError, match="No such file or directory: 'not-an-experiment.expr'"):
		read_expr_list("not-an-experiment.expr")
	with pytest.raises(FileNotFoundError, match="No such file or directory: .*__init__.py.*"):
		read_expr_list("__init__.py")
