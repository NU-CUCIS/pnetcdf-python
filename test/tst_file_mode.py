# This file is part of pncpy, a Python interface to the PnetCDF library.
#
#
# Copyright (C) 2023, Northwestern University
# See COPYRIGHT notice in top-level directory
# License:  

"""
   This example program is intended to illustrate the use of the pnetCDF python API.
   It is a program which creates or opens a netCDF file using the `File` constructor
   with different access modes


   To run the test, execute the following
    `mpiexec -n [num_process] python3  tst_file_mode.py [test_file_output_dir](optional)`

"""
import pncpy
from numpy.random import seed, randint
from numpy.testing import assert_array_equal, assert_equal, assert_array_almost_equal
import tempfile, unittest, os, random, sys
import numpy as np
from mpi4py import MPI
from utils import validate_nc_file

seed(0)
# Format of the data file we will create (64BIT_DATA for CDF-5 and 64BIT_OFFSET for CDF-2 and None for CDF-1)
data_models = ['64BIT_DATA', '64BIT_OFFSET', None]
# Name of the test data file
file_name = "tst_file_mode.nc"
xdim = 9
ydim = 10
zdim = 11
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()




class VariablesTestCase(unittest.TestCase):

    def setUp(self):
        if (len(sys.argv) == 2) and os.path.isdir(sys.argv[1]):
            self.file_path = os.path.join(sys.argv[1], file_name)
        else:
            self.file_path = file_name
        self.data_model = data_models.pop(0)

        

    def tearDown(self):
        # Wait for all processes to finish testing (in multiprocessing mode)
        comm.Barrier()
        # Remove testing file
        if (rank == 0) and not((len(sys.argv) == 2) and os.path.isdir(sys.argv[1])):
            os.remove(self.file_path)

    def test_cdf5(self):
        """testing file access with different modes in CDF5 data file"""
        # TEST MODE "w"
        with pncpy.File(filename=self.file_path, mode='w', format=self.data_model, Comm=comm) as f:
        # Try writing to file by defining a dimension
            f.defineDim('x',xdim)
        # Validate the created data file using ncvalidator tool
        comm.Barrier()
        assert validate_nc_file(self.file_path) == 0

        # TEST MODE "r"
        with pncpy.File(filename=self.file_path, mode='r') as f:
        # Try writing to file by defining a dimension
            try:
                f.redef()
                f.defineDim('x',xdim)
            except RuntimeError:
                pass
            else:
                raise RuntimeError("Attempting to write data with 'r' access mode should failed")
            #Reading should be allowed. Check if 'x' dimension existed in file
            self.assertTrue('x' in f.dimensions.keys())
        
        # TEST MODE "r+"
        with pncpy.File(filename=self.file_path, mode='r+') as f:
            f.redef()
            # Try writing to file by defining a dimension
            f.defineDim('y',ydim)
            # Check if both 'x' and 'y' dimensions existed in file
            self.assertTrue('x' in f.dimensions.keys())
            self.assertTrue('y' in f.dimensions.keys())
        comm.Barrier()
        assert validate_nc_file(self.file_path) == 0


        # TEST MODE "a"
        with pncpy.File(filename=self.file_path, mode='a') as f:
            f.redef()
            # Try writing to file by defining a dimension
            f.defineDim('z',zdim)
            # Check if both 'x' and 'y' dimensions existed in file
            self.assertTrue('x' in f.dimensions.keys())
            self.assertTrue('y' in f.dimensions.keys())
            self.assertTrue('z' in f.dimensions.keys())
        comm.Barrier()
        assert validate_nc_file(self.file_path) == 0

        # TEST MODE "x"
        # Try create a new file with the same name using mode "x"
        try:
            f = pncpy.File(filename=self.file_path, mode='x')
        except OSError:
            pass
        else:
            raise RuntimeError("This should have failed")

    def test_cdf2(self):
        """testing file access with different modes in CDF2 data file"""
        # TEST MODE "w"
        with pncpy.File(filename=self.file_path, mode='w', format=self.data_model, Comm=comm) as f:
        # Try writing to file by defining a dimension
            f.defineDim('x',xdim)
        # Validate the created data file using ncvalidator tool
        comm.Barrier()
        assert validate_nc_file(self.file_path) == 0

        # TEST MODE "r"
        with pncpy.File(filename=self.file_path, mode='r') as f:
        # Try writing to file by defining a dimension
            try:
                f.redef()
                f.defineDim('x',xdim)
            except RuntimeError:
                pass
            else:
                raise RuntimeError("Attempting to write data with 'r' access mode should failed")
            #Reading should be allowed. Check if 'x' dimension existed in file
            self.assertTrue('x' in f.dimensions.keys())
        
        # TEST MODE "r+"
        with pncpy.File(filename=self.file_path, mode='r+') as f:
            f.redef()
            # Try writing to file by defining a dimension
            f.defineDim('y',ydim)
            # Check if both 'x' and 'y' dimensions existed in file
            self.assertTrue('x' in f.dimensions.keys())
            self.assertTrue('y' in f.dimensions.keys())
        comm.Barrier()
        assert validate_nc_file(self.file_path) == 0


        # TEST MODE "a"
        with pncpy.File(filename=self.file_path, mode='a') as f:
            f.redef()
            # Try writing to file by defining a dimension
            f.defineDim('z',zdim)
            # Check if both 'x' and 'y' dimensions existed in file
            self.assertTrue('x' in f.dimensions.keys())
            self.assertTrue('y' in f.dimensions.keys())
            self.assertTrue('z' in f.dimensions.keys())
        comm.Barrier()
        assert validate_nc_file(self.file_path) == 0

        # TEST MODE "x"
        # Try create a new file with the same name using mode "x"
        try:
            f = pncpy.File(filename=self.file_path, mode='x')
        except OSError:
            pass
        else:
            raise RuntimeError("This should have failed")

    def test_cdf1(self):
        """testing file access with different modes in CDF1 data file"""
        # TEST MODE "w"
        with pncpy.File(filename=self.file_path, mode='w', format=self.data_model, Comm=comm) as f:
        # Try writing to file by defining a dimension
            f.defineDim('x',xdim)
        # Validate the created data file using ncvalidator tool
        comm.Barrier()
        assert validate_nc_file(self.file_path) == 0

        # TEST MODE "r"
        with pncpy.File(filename=self.file_path, mode='r') as f:
        # Try writing to file by defining a dimension
            try:
                f.redef()
                f.defineDim('x',xdim)
            except RuntimeError:
                pass
            else:
                raise RuntimeError("Attempting to write data with 'r' access mode should failed")
            #Reading should be allowed. Check if 'x' dimension existed in file
            self.assertTrue('x' in f.dimensions.keys())
        
        # TEST MODE "r+"
        with pncpy.File(filename=self.file_path, mode='r+') as f:
            f.redef()
            # Try writing to file by defining a dimension
            f.defineDim('y',ydim)
            # Check if both 'x' and 'y' dimensions existed in file
            self.assertTrue('x' in f.dimensions.keys())
            self.assertTrue('y' in f.dimensions.keys())
        comm.Barrier()
        assert validate_nc_file(self.file_path) == 0


        # TEST MODE "a"
        with pncpy.File(filename=self.file_path, mode='a') as f:
            f.redef()
            # Try writing to file by defining a dimension
            f.defineDim('z',zdim)
            # Check if both 'x' and 'y' dimensions existed in file
            self.assertTrue('x' in f.dimensions.keys())
            self.assertTrue('y' in f.dimensions.keys())
            self.assertTrue('z' in f.dimensions.keys())
        comm.Barrier()
        assert validate_nc_file(self.file_path) == 0

        # TEST MODE "x"
        # Try create a new file with the same name using mode "x"
        try:
            f = pncpy.File(filename=self.file_path, mode='x')
        except OSError:
            pass
        else:
            raise RuntimeError("This should have failed")


# Unittest execution order: setUp -> test_cdf5 -> tearDown -> setUp -> test_cdf2 -> tearDown
if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0]])