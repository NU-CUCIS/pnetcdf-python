import pncpy
from numpy.random import seed, randint
from numpy.testing import assert_array_equal, assert_equal,\
assert_array_almost_equal
import tempfile, unittest, os, random, sys
import numpy as np
from mpi4py import MPI
from utils import validate_nc_file

seed(0)
data_models = ['64BIT_DATA', '64BIT_OFFSET', None]
file_name = "tst_var_get_var.nc"
xdim=9; ydim=10; zdim=11
data = randint(0,10, size=(xdim,ydim,zdim)).astype('i4')
datarev = data[:,::-1,:].copy()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()



class VariablesTestCase(unittest.TestCase):

    def setUp(self):
        if (len(sys.argv) == 2) and os.path.isdir(sys.argv[1]):
            self.file_path = os.path.join(sys.argv[1], file_name)
        else:
            self.file_path = file_name
        data_model = data_models.pop(0)
        f = pncpy.File(filename=self.file_path, mode = 'w', format=data_model, Comm=comm, Info=None)
        f.defineDim('x',xdim)
        f.defineDim('xu',-1)
        f.defineDim('y',ydim)
        f.defineDim('z',zdim)

        v1 = f.defineVar('data1', pncpy.NC_INT, ('x','y','z'))

        #initize variable values
        f.enddef()
        v1[:,::-1,:] = data
        f.close()
        comm.Barrier()
        assert validate_nc_file(self.file_path) == 0

    def tearDown(self):
        # Remove the temporary files
        comm.Barrier()
        if (rank == 0) and not((len(sys.argv) == 2) and os.path.isdir(sys.argv[1])):
            os.remove(self.file_path)


    def test_cdf5(self):
        """testing variable put var1 all"""
        f = pncpy.File(self.file_path, 'r')
        v1 = f.variables['data1']
        # test collective i/o put_var1
        f.begin_indep()
        if rank < 2:
            v1_data = v1.get_var()
            assert_equal(v1_data, datarev)
        # test independent i/o put_var1
        f.end_indep()
        v1_data = v1.get_var_all()
        assert_equal(v1_data, datarev)
        f.close()


    def test_cdf2(self):
        """testing variable put var1 all"""
        f = pncpy.File(self.file_path, 'r')
        v1 = f.variables['data1']
        # test collective i/o put_var1
        f.begin_indep()
        if rank < 2:
            v1_data = v1.get_var()
            assert_equal(v1_data, datarev)
        # test independent i/o put_var1
        f.end_indep()
        v1_data = v1.get_var_all()
        assert_equal(v1_data, datarev)
        f.close()

    def test_cdf1(self):
        """testing variable put var1 all"""
        f = pncpy.File(self.file_path, 'r')
        v1 = f.variables['data1']
        # test collective i/o put_var1
        f.begin_indep()
        if rank < 2:
            v1_data = v1.get_var()
            assert_equal(v1_data, datarev)
        # test independent i/o put_var1
        f.end_indep()
        v1_data = v1.get_var_all()
        assert_equal(v1_data, datarev)
        f.close()


if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0]])
