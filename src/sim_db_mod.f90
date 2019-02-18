!> @file sim_db_mod.f90
!> @brief The Fortran class and functions to use ```sim_db```.

! Copyright (C) 2019 Håkon Austlid Taskén <hakon.tasken@gmail.com>
! Licensed under the MIT License.

module sim_db_mod !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

use, intrinsic :: iso_c_binding, only : c_ptr, c_int, c_double, c_bool, &
    c_char, c_size_t, c_null_char, c_loc, c_f_pointer
use, intrinsic :: iso_fortran_env
use sim_db_c_interface
implicit none

private
public :: sim_db, sim_db_add_empty_sim

!> Class to interact with the **sim_db** database.
!>
!> Constructor is an overload of the **sim_db_dtor\*** functions below, which
!> gives the valid types of parameters.
!>
!> Should be called at the very begin of the simulation and
!> **close** should be called at the very end to add the correct metadata and 
!> to clean up.
!>
!> For multithreading/multiprocessing each thread/process MUST have its
!> own connection (instance of this class).
type, public :: sim_db
    type(c_ptr), private :: sim_db_ptr
contains
    !> Read parameter from database. 
    !>
    !> Overload of the **read_\*** subroutines below, which gives the valid types 
    !> of parameters.
    generic :: read => read_int, read_real_sp, read_real_dp, read_string, &
        read_logical, read_int_array, read_real_sp_array, read_real_dp_array, &
        read_string_array, read_logical_array
    procedure :: read_int
    procedure :: read_real_sp
    procedure :: read_real_dp
    procedure :: read_string
    procedure :: read_logical
    procedure :: read_int_array
    procedure :: read_real_sp_array
    procedure :: read_real_dp_array
    procedure :: read_string_array
    procedure :: read_logical_array

    !> Write parameter to database.
    !>
    !> Overload of the **write_\*** below, which gives the valid types of 
    !> parameters.
    generic :: write => write_int, write_real_sp, write_real_dp, write_string, &
        write_logical, write_int_array, write_real_sp_array, &
        write_real_dp_array, write_string_array, write_logical_array, &
        write_int_false, write_real_sp_false, write_real_dp_false, &
        write_string_false, write_logical_false, write_int_array_false, &
        write_real_sp_array_false, write_real_dp_array_false, &
        write_string_array_false, write_logical_array_false
    procedure :: write_int
    procedure :: write_real_sp
    procedure :: write_real_dp
    procedure :: write_string
    procedure :: write_logical
    procedure :: write_int_array
    procedure :: write_real_sp_array
    procedure :: write_real_dp_array
    procedure :: write_string_array
    procedure :: write_logical_array
    procedure :: write_int_false
    procedure :: write_real_sp_false
    procedure :: write_real_dp_false
    procedure :: write_string_false
    procedure :: write_logical_false
    procedure :: write_int_array_false
    procedure :: write_real_sp_array_false
    procedure :: write_real_dp_array_false
    procedure :: write_string_array_false
    procedure :: write_logical_array_false

    procedure :: unique_results_dir
    procedure :: unique_results_dir_abs_path
    procedure :: column_exists
    procedure :: is_empty
    procedure :: set_empty
    procedure :: get_id
    procedure :: get_path_proj_root

    !> Save the sha1 hash of the files \p paths_executables to the database.
    !> 
    !> Overload of the **update_sha1_executables_\*** functions, which gives 
    !> the valid types of parameters.
    generic :: update_sha1_executables => &
        update_sha1_executables_conditionally, &
        update_sha1_executables_unconditionally
    procedure :: update_sha1_executables_conditionally
    procedure :: update_sha1_executables_unconditionally

    procedure :: allow_timeouts
    procedure :: have_timed_out
    procedure :: delete_from_database
    procedure :: close
    final :: sim_db_dtor
end type sim_db

interface sim_db
    module procedure sim_db_ctor
    module procedure sim_db_ctor_with_id
    module procedure sim_db_ctor_without_search
end interface sim_db

interface sim_db_add_empty_sim
    procedure sim_db_add_empty_sim_with_search, &
              sim_db_add_empty_sim_without_search, &
              sim_db_add_empty_sim_without_search_false
end interface sim_db_add_empty_sim

type, private :: c_string
    character(len=:), pointer :: c_str
contains
    procedure, private :: to_c_ptr
    final :: c_string_dtor
end type c_string

interface c_string
    module procedure c_string_ctor
end interface c_string

contains !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!> Connect to the database using the command line arguments containing 
!> ```--id 'ID'``` and optionally ```--path_proj_root 'PATH'```. *PATH* is the 
!> root directory of the project, where *.sim_db/* is located. If not passed, 
!> the current working directory and its parent directories will be searched 
!> until *.sim_db/* is found.
!>
!> @param store_metadata **logical, optional** Stores metadata to database if 
!> true. Set to 'false' for postprocessing (e.g. visualization) of data from 
!> simulation.
function sim_db_ctor(store_metadata) result(sim_database)
    logical, optional, value :: store_metadata
    type(sim_db) :: sim_database

    integer :: i, nargs, len_str
    character(len=100, kind=c_char), dimension(:), allocatable, target :: &
        command_line_arguments
    type(c_ptr), dimension(:), allocatable, target :: argv

    if (.not. present(store_metadata)) store_metadata = .true.

    nargs = command_argument_count()
    allocate(command_line_arguments(nargs))
    allocate(argv(nargs))

    do i = 1, nargs
        call get_command_argument(i, command_line_arguments(i))
        len_str = len_trim(command_line_arguments(i))
        if (len_str >= 100) then
            error stop "ERROR: Command line argument longer than the maximum &
                       &100 characters."
        end if
        command_line_arguments(i)(len_str + 1:len_str + 1) = c_null_char
        argv(i) = c_loc(command_line_arguments(i))
    end do

    if (store_metadata) then
        sim_database%sim_db_ptr = sim_db_ctor_c(nargs, argv)
    else
        sim_database%sim_db_ptr = sim_db_ctor_no_metadata_c(nargs, argv)
    end if

    deallocate(argv)
    deallocate(command_line_arguments)
end function sim_db_ctor

!> @param id **integer, intent(in)** ID number of the simulation paramters in 
!> the **sim_db** database.
!> @param store_metadata **logical, optional** Stores metadata to database if 
!> true. Set to 'false' for postprocessing (e.g. visualization) of data from 
!> simulation.
function sim_db_ctor_with_id(id, store_metadata) result(sim_database)
    integer, value, intent(in) :: id
    logical, optional, value :: store_metadata
    type(sim_db) :: sim_database

    if (.not. present(store_metadata)) store_metadata = .true.

    sim_database%sim_db_ptr = sim_db_ctor_with_id_c(int(id, kind=c_int), &
                                           logical(store_metadata, kind=c_bool))
end function sim_db_ctor_with_id

!> @param path_proj_root **character(len=*), intent(in)** Path to the root 
!> directory of the project, where *.sim_db/* is located.
!> @param id **integer, intent(in)** ID number of the simulation paramters in the **sim_db**
!> database.
!> @param store_metadata **logical, optional** Stores metadata to database if 
!> true. Set to 'false' for postprocessing (e.g. visualization) of data from 
!> simulation.
function sim_db_ctor_without_search(path_proj_root, id, store_metadata) &
        result(sim_database)
    character(len=*), intent(in) :: path_proj_root
    integer, value, intent(in) :: id
    logical, optional, value :: store_metadata
    type(sim_db) :: sim_database

    type(c_string) :: path_proj_root_c_str
    path_proj_root_c_str = c_string(path_proj_root)

    if (.not. present(store_metadata)) store_metadata = .true.

    sim_database%sim_db_ptr = sim_db_ctor_without_search_c( &
            path_proj_root_c_str%to_c_ptr(), int(id, kind=c_int), &
            logical(store_metadata, kind=c_bool))
end function sim_db_ctor_without_search

!> @param[in] column **character(len=*), intent(in)** Name of the parameter and 
!> column in the database.
!> @param[out] int_value **integer, intent(out)**  Value read from database.
subroutine read_int(self, column, int_value)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    integer, intent(out) :: int_value

    type(c_string) :: column_c_str
    column_c_str = c_string(column)

    int_value = int(sim_db_read_int_c(self%sim_db_ptr, column_c_str%to_c_ptr()))
end subroutine read_int

!> @param[in] column **character(len=*), intent(in)** Name of the parameter and 
!> column in the database.
!> @param[out] real_value **real(kind=kind(1.0d0)), intent(out)**  Value read from 
!> database.
subroutine read_real_dp(self, column, real_value)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    real(kind=kind(1.0d0)), intent(out) :: real_value

    type(c_string) :: column_c_str
    column_c_str = c_string(column)

    real_value = real(sim_db_read_double_c(self%sim_db_ptr, &
                      column_c_str%to_c_ptr()), kind(1.0d0))
end subroutine read_real_dp

!> @param[in] column **character(len=*), intent(in)** Name of the parameter and 
!> column in the database.
!> @param[out] real_value **real, intent(out)** Value read from database.
subroutine read_real_sp(self, column, real_value)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    real, intent(out) :: real_value

    real(kind=kind(1.0d0)) real_dp_value

    call read_real_dp(self, column, real_dp_value)
    real_value = real(real_dp_value)
end subroutine read_real_sp

!> @param[in] column **character(len=*), intent(in)** Name of the parameter and 
!> column in the database.
!> @param[out] string_value **character(len=:), allocatable, intent(out)** Value read from database.
subroutine read_string(self, column, string_value)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    character(len=:), allocatable, intent(out) :: string_value

    type(c_ptr) :: c_str
    character(len=huge(0), kind=c_char), pointer :: f_str
    type(c_string) :: column_c_str
    column_c_str = c_string(column)

    c_str = sim_db_read_string_c(self%sim_db_ptr, column_c_str%to_c_ptr())
    call c_f_pointer(c_str, f_str)
    string_value = f_str(1:index(f_str, c_null_char) - 1)
end subroutine read_string

!> @param[in] column **character(len=*), intent(in)** Name of the parameter and 
!> column in the database.
!> @param[out] logical_value **logical, intent(out)** Value read from database.
subroutine read_logical(self, column, logical_value)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    logical, intent(out) :: logical_value

    type(c_string) :: column_c_str
    column_c_str = c_string(column)

    logical_value = sim_db_read_bool_c(self%sim_db_ptr, column_c_str%to_c_ptr())
end subroutine read_logical

!> @param[in] column **character(len=*), intent(in)** Name of the parameter and 
!> column in the database.
!> @param[out] int_array **integer, dimension(:), allocatable, intent(out)** Value read from database.
subroutine read_int_array(self, column, int_array)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    integer, dimension(:), allocatable, intent(out) :: int_array

    type(sim_db_vec) :: c_int_vec
    integer(kind=c_int), dimension(:), pointer :: int_array_ptr
    integer :: i
    type(c_string) :: column_c_str

    column_c_str = c_string(column)
    c_int_vec = sim_db_read_int_vec_c(self%sim_db_ptr, column_c_str%to_c_ptr())
    call c_f_pointer(c_int_vec%array, int_array_ptr, [c_int_vec%size])
    int_array = int_array_ptr
end subroutine read_int_array

!> @param[in] column **character(len=*), intent(in)** Name of the parameter and 
!> column in the database.
!> @param[out] real_array **real, dimension(:), allocatable, intent(out)** Value read from database.
subroutine read_real_sp_array(self, column, real_array)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    real, dimension(:), allocatable, intent(out) :: real_array

    type(sim_db_vec) :: c_double_vec
    real(kind=c_double), dimension(:), pointer :: real_array_ptr
    integer :: i 
    type(c_string) :: column_c_str

    column_c_str = c_string(column)
    c_double_vec = sim_db_read_double_vec_c(self%sim_db_ptr, column_c_str%to_c_ptr())
    call c_f_pointer(c_double_vec%array, real_array_ptr, [c_double_vec%size])
    real_array = real_array_ptr
end subroutine read_real_sp_array

!> @param[in] column **character(len=*), intent(in)** Name of the parameter and 
!> column in the database.
!> @param[out] real_array **real(kind=kind(1.0d0)), dimension(:), allocatable, intent(out)** Value read from database.
subroutine read_real_dp_array(self, column, real_array)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    real(kind=kind(1.0d0)), dimension(:), allocatable, intent(out) :: real_array

    type(sim_db_vec) :: c_double_vec
    real(kind=c_double), dimension(:), pointer :: real_array_ptr
    integer :: i 
    type(c_string) :: column_c_str

    column_c_str = c_string(column)
    c_double_vec = sim_db_read_double_vec_c(self%sim_db_ptr, &
                                            column_c_str%to_c_ptr())
    call c_f_pointer(c_double_vec%array, real_array_ptr, [c_double_vec%size])
    real_array = real_array_ptr
end subroutine read_real_dp_array

!> @param[in] column **character(len=*), intent(in)** Name of the parameter and 
!> column in the database.
!> @param[out]  **allocatable, intent(out) :: string_array character(len(:), dimension(** Value read from databas.
subroutine read_string_array(self, column, string_array)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    character(len=:), dimension(:), allocatable, intent(out) :: string_array

    type(sim_db_vec) :: c_string_vec
    type(c_ptr), dimension(:), pointer :: c_str_array_ptr
    character(len=huge(0), kind=c_char), pointer :: f_str
    integer :: i, len_str, max_len_str
    type(c_string) :: column_c_str

    column_c_str = c_string(column)
    c_string_vec = sim_db_read_string_vec_c(self%sim_db_ptr, &
                                            column_c_str%to_c_ptr())
    call c_f_pointer(c_string_vec%array, c_str_array_ptr, [c_string_vec%size])
    max_len_str = 0
    do i = 1, size(c_str_array_ptr)
        call c_f_pointer(c_str_array_ptr(i), f_str)
        len_str = index(f_str, c_null_char)
        if (len_str > max_len_str) then 
            max_len_str = len_str
        end if
    end do
    allocate(character(max_len_str) :: string_array(c_string_vec%size))
    do i = 1, size(string_array)
        call c_f_pointer(c_str_array_ptr(i), f_str)
        string_array(i) = f_str(1:index(f_str, c_null_char) - 1)
    end do
end subroutine read_string_array

!> @param[in] column **character(len=*), intent(in)** Name of the parameter and 
!> column in the database.
!> @param[out] logical_array **logical, dimension(:), allocatable, intent(out)** 
!> Value read from database.
subroutine read_logical_array(self, column, logical_array)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    logical, dimension(:), allocatable, intent(out) :: logical_array

    type(sim_db_vec) :: c_bool_vec
    logical(kind=c_bool), dimension(:), pointer :: logical_array_ptr
    integer :: i 
    type(c_string) :: column_c_str
    column_c_str = c_string(column)
    c_bool_vec = sim_db_read_bool_vec_c(self%sim_db_ptr, column_c_str%to_c_ptr())
    call c_f_pointer(c_bool_vec%array, logical_array_ptr, [c_bool_vec%size])
    logical_array = logical_array_ptr
end subroutine read_logical_array

!> @param column **character(len=*), intent(in)** Name of the parameter and 
!> column in the database.
!> @param int_value **integer, intent(in)** To be written to database.
!> @param only_if_empty **logical** If .true., it will only write to the 
!> database if the simulation's entry under 'column' is empty. Will avoid
!> potential timeouts for concurrect applications.
subroutine write_int(self, column, int_value, only_if_empty)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    integer, intent(in) :: int_value
    logical, value :: only_if_empty

    type(c_string) :: column_c_str
    column_c_str = c_string(column)
    call sim_db_write_int_c(self%sim_db_ptr, column_c_str%to_c_ptr(), &
        int(int_value, kind=c_int), logical(only_if_empty, kind=c_bool))
end subroutine write_int

!> @param column **character(len=*), intent(in)** Name of the parameter and 
!> column in the database.
!> @param int_value **integer, intent(in)** To be written to database.
subroutine write_int_false(self, column, int_value)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    integer, intent(in) :: int_value
    call write_int(self, column, int_value, .false.)
end subroutine write_int_false

!> @param column **character(len=*), intent(in)** Name of the parameter and 
!> column in the database.
!> @param real_value **real, intent(in)** To be written to database.
!> @param only_if_empty **logical** If .true., it will only write to the 
!> database if the simulation's entry under 'column' is empty. Will avoid
!> potential timeouts for concurrect applications.
subroutine write_real_sp(self, column, real_value, only_if_empty)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    real, intent(in) :: real_value
    logical, value :: only_if_empty

    type(c_string) :: column_c_str
    column_c_str = c_string(column)
    call sim_db_write_double_c(self%sim_db_ptr, column_c_str%to_c_ptr(), &
        real(real_value, kind=c_double), logical(only_if_empty, kind=c_bool))
end subroutine write_real_sp

!> @param column **character(len=*), intent(in)** Name of the parameter and
!> column in the database.
!> @param real_value **real, intent(in)** To be written to database.
subroutine write_real_sp_false(self, column, real_value)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    real, intent(in) :: real_value
    call write_real_sp(self, column, real_value, .false.)
end subroutine write_real_sp_false

!> @param column **character(len=*), intent(in)** Name of the parameter and
!> column in the database.
!> @param real_value **real(kind=kind(1.0d0)), intent(in)** To be written to database.
!> @param only_if_empty **logical** If .true., it will only write to the 
!> database if the simulation's entry under 'column' is empty. Will avoid
!> potential timeouts for concurrect applications.
subroutine write_real_dp(self, column, real_value, only_if_empty)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    real(kind=kind(1.0d0)), intent(in) :: real_value
    logical, value :: only_if_empty

    type(c_string) :: column_c_str
    column_c_str = c_string(column)
    call sim_db_write_double_c(self%sim_db_ptr, column_c_str%to_c_ptr(), &
        real(real_value, kind=c_double), logical(only_if_empty, kind=c_bool))
end subroutine write_real_dp

!> @param column **character(len=*), intent(in)** Name of the parameter and
!> column in the database.
!> @param real_value **real(kind=kind(1.0d0)), intent(in)** To be written to database.
subroutine write_real_dp_false(self, column, real_value)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    real(kind=kind(1.0d0)), intent(in) :: real_value
    call write_real_dp(self, column, real_value, .false.)
end subroutine write_real_dp_false

!> @param column **character(len=*), intent(in)** Name of the parameter and
!> column in the database.
!> @param string_value **character(len=*), intent(in)** To be written to database.
!> @param only_if_empty **logical** If .true., it will only write to the 
!> database if the simulation's entry under 'column' is empty. Will avoid
!> potential timeouts for concurrect applications.
subroutine write_string(self, column, string_value, only_if_empty)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    character(len=*), intent(in) :: string_value
    logical, value :: only_if_empty

    type(c_string) :: column_c_str, string_value_c_str
    column_c_str = c_string(column)
    string_value_c_str = c_string(string_value)
    call sim_db_write_string_c(self%sim_db_ptr, column_c_str%to_c_ptr(), &
        string_value_c_str%to_c_ptr(), logical(only_if_empty, kind=c_bool))
end subroutine write_string

!> @param column **character(len=*), intent(in)** Name of the parameter and
!> column in the database.
!> @param string_value **character(len=*), intent(in)** To be written to database.
subroutine write_string_false(self, column, string_value)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    character(len=*), intent(in) :: string_value
    call write_string(self, column, string_value, .false.)
end subroutine write_string_false

!> @param column **character(len=*), intent(in)** Name of the parameter and
!> column in the database.
!> @param logical_value **logical, intent(in)** To be written to database.
!> @param only_if_empty **logical** If .true., it will only write to the 
!> database if the simulation's entry under 'column' is empty. Will avoid
!> potential timeouts for concurrect applications.
subroutine write_logical(self, column, logical_value, only_if_empty)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    logical, intent(in) :: logical_value
    logical, value :: only_if_empty

    type(c_string) :: column_c_str
    column_c_str = c_string(column)
    call sim_db_write_bool_c(self%sim_db_ptr, column_c_str%to_c_ptr(), &
        logical(logical_value, kind=c_bool), logical(only_if_empty, kind=c_bool))
end subroutine write_logical

!> @param column **character(len=*), intent(in)** Name of the parameter and
!> column in the database.
!> @param logical_value **logical, intent(in)** To be written to database.
subroutine write_logical_false(self, column, logical_value)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    logical, intent(in) :: logical_value
    call write_logical(self, column, logical_value, .false.)
end subroutine write_logical_false

!> @param column **character(len=*), intent(in)** Name of the parameter and
!> column in the database.
!> @param int_array **integer, dimension(:), intent(in)** To be written to database.
!> @param only_if_empty **logical** If .true., it will only write to the 
!> database if the simulation's entry under 'column' is empty. Will avoid
!> potential timeouts for concurrect applications.
subroutine write_int_array(self, column, int_array, only_if_empty)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    integer, dimension(:), intent(in) :: int_array
    logical, intent(in) :: only_if_empty

    integer(c_int), dimension(:), allocatable, target :: c_int_array
    integer :: i 
    type(c_string) :: column_c_str
    if (c_int == kind(1)) then
            c_int_array = int_array
    else
        allocate(c_int_array(size(int_array)))
        do i = 1, size(c_int_array)
            c_int_array(i) = int(int_array(i), kind=c_int)
        end do
    end if
    column_c_str = c_string(column)
    call sim_db_write_int_array_c(self%sim_db_ptr, column_c_str%to_c_ptr(), &
                                     c_loc(c_int_array), size(c_int_array), &
                                     logical(only_if_empty, kind=c_bool))
end subroutine write_int_array

!> @param column **character(len=*), intent(in)** Name of the parameter and
!> column in the database.
!> @param int_array **integer, dimension(:), target, intent(in)** To be written to database.
subroutine write_int_array_false(self, column, int_array)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    integer, dimension(:), target, intent(in) :: int_array
    call write_int_array(self, column, int_array, .false.)
end subroutine write_int_array_false

!> @param column **character(len=*), intent(in)** Name of the parameter and
!> column in the database.
!> @param real_array **real(kind=kind(1.0d0)), dimension(:), intent(in)** To be written to database.
!> @param only_if_empty **logical** If .true., it will only write to the 
!> database if the simulation's entry under 'column' is empty. Will avoid
!> potential timeouts for concurrect applications.
subroutine write_real_dp_array(self, column, real_array, only_if_empty)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    real(kind=kind(1.0d0)), dimension(:), intent(in) :: real_array
    logical, intent(in) :: only_if_empty

    real(c_double), dimension(:), allocatable, target :: c_double_array
    integer :: i 
    type(c_string) :: column_c_str
    if (c_double == kind(1.0d0)) then
            c_double_array = real_array
    else
        allocate(c_double_array(size(real_array)))
        do i = 1, size(c_double_array)
            c_double_array(i) = real(real_array(i), kind=c_double)
        end do
    end if
    column_c_str = c_string(column)
    call sim_db_write_double_array_c(self%sim_db_ptr, column_c_str%to_c_ptr(), &
                                  c_loc(c_double_array), size(c_double_array), &
                                     logical(only_if_empty, kind=c_bool))
end subroutine write_real_dp_array

!> @param column **character(len=*), intent(in)** Name of the parameter and
!> column in the database.
!> @param real_array **real(kind=kind(1.0d0)), dimension(:), target, intent(in)** To be written to database.
subroutine write_real_dp_array_false(self, column, real_array)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    real(kind=kind(1.0d0)), dimension(:), target, intent(in) :: real_array
    call write_real_dp_array(self, column, real_array, .false.)
end subroutine write_real_dp_array_false

!> @param column **character(len=*), intent(in)** Name of the parameter and
!> column in the database.
!> @param real_array **real, dimension(:), intent(in)** To be written to database.
!> @param only_if_empty **logical** If .true., it will only write to the 
!> database if the simulation's entry under 'column' is empty. Will avoid
!> potential timeouts for concurrect applications.
subroutine write_real_sp_array(self, column, real_array, only_if_empty)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    real, dimension(:), intent(in) :: real_array
    logical, intent(in) :: only_if_empty

    real(c_double), dimension(:), allocatable, target :: c_double_array
    integer :: i 
    type(c_string) :: column_c_str
    if (c_double == kind(1.0)) then
        c_double_array = real_array
    else
        allocate(c_double_array(size(real_array)))
        do i = 1, size(c_double_array)
            c_double_array(i) = real(real_array(i), kind=c_double)
        end do
    end if
    column_c_str = c_string(column)
    call sim_db_write_double_array_c(self%sim_db_ptr, column_c_str%to_c_ptr(), &
                                  c_loc(c_double_array), size(c_double_array), &
                                     logical(only_if_empty, kind=c_bool))
end subroutine write_real_sp_array

!> @param column **character(len=*), intent(in)** Name of the parameter and
!> column in the database.
!> @param real_array **real, dimension(:), intent(in)** To be written to database.
subroutine write_real_sp_array_false(self, column, real_array)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    real, dimension(:), intent(in) :: real_array
    call write_real_sp_array(self, column, real_array, .false.)
end subroutine write_real_sp_array_false

!> @param column **character(len=*), intent(in)** Name of the parameter and
!> column in the database.
!> @param string_array **character(len=*), dimension(:), intent(in)** n=*), dimension**(To be written to database.
!> @param only_if_empty **logical** If .true., it will only write to the 
!> database if the simulation's entry under 'column' is empty. Will avoid
!> potential timeouts for concurrect applications.
subroutine write_string_array(self, column, string_array, only_if_empty)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    character(len=*), dimension(:), intent(in) :: string_array
    logical, intent(in) :: only_if_empty

    type(c_ptr), dimension(:), allocatable, target :: c_ptr_array
    integer :: i
    type(c_string) :: c_str, column_c_str

    allocate(c_ptr_array(size(string_array)))
    do i = 1, size(string_array)
        c_str = c_string(string_array(i))
        c_ptr_array(i) = c_str%to_c_ptr()
    end do

    column_c_str = c_string(column)
    column_c_str = c_string(column)
    call sim_db_write_string_array_c(self%sim_db_ptr, column_c_str%to_c_ptr(), &
                                     c_loc(c_ptr_array), size(string_array), &
                                     logical(only_if_empty, kind=c_bool))

    deallocate(c_ptr_array)
end subroutine write_string_array

!> @param column **character(len=*), intent(in)** Name of the parameter and
!> column in the database.
!> @param intent **character(len=*), dimension**(To be written to database.
subroutine write_string_array_false(self, column, string_array)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    character(len=*), dimension(:), intent(in) :: string_array
    call write_string_array(self, column, string_array, .false.)
end subroutine write_string_array_false

!> @param column **character(len=*), intent(in)** Name of the parameter and
!> column in the database.
!> @param logical_array **logical, dimension(:), intent(in)** To be written to database.
!> @param only_if_empty **logical** If .true., it will only write to the 
!> database if the simulation's entry under 'column' is empty. Will avoid
!> potential timeouts for concurrect applications.
subroutine write_logical_array(self, column, logical_array, only_if_empty)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    logical, dimension(:), intent(in) :: logical_array
    logical, intent(in) :: only_if_empty

    logical(c_bool), dimension(:), allocatable, target :: c_bool_array
    integer :: i 
    type(c_string) :: column_c_str
    if (c_bool == kind(.true.)) then
            c_bool_array = logical_array
    else
        allocate(c_bool_array(size(logical_array)))
        do i = 1, size(c_bool_array)
            c_bool_array(i) = logical(logical_array(i), kind=c_bool)
        end do
    end if

    column_c_str = c_string(column)
    c_bool_array = logical_array
    call sim_db_write_bool_array_c(self%sim_db_ptr, column_c_str%to_c_ptr(), &
                                     c_loc(c_bool_array), size(c_bool_array), &
                                     logical(only_if_empty, kind=c_bool))
end subroutine write_logical_array

!> @param column **character(len=*), intent(in)** Name of the parameter and
!> column in the database.
!> @param logical_array **logical, dimension(:), intent(in)** To be written to database.
subroutine write_logical_array_false(self, column, logical_array)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    logical, dimension(:), intent(in) :: logical_array
    call write_logical_array(self, column, logical_array, .false.)
end subroutine write_logical_array_false

!> Get path to subdirectory in \p path_directory unique to simulation.
!>
!> The subdirectory will be named 'date_time_name_id' and is intended to
!> store results in. If 'results_dir' in the database is empty, a new and
!> unique directory is created and the path stored in 'results_dir'.
!> Otherwise the path in 'results_dir' is just returned.
!>
!> @param path_directory **character(len=*), intent(in)** Path to where the new 
!> directory is created. If it starts with 'root/', that part will be replaced 
!> with the full path to the root directory of the project.
!> @return **character(len=:), allocatable** Path to new subdirectory.
function unique_results_dir(self, path_to_dir)
    class(sim_db)::self
    character(len=*), intent(in) :: path_to_dir
    character(len=:), allocatable :: unique_results_dir

    type(c_ptr) :: c_str
    character(len=huge(0), kind=c_char), pointer :: f_str
    type(c_string) :: path_c_str
    path_c_str = c_string(path_to_dir)

    c_str = sim_db_unique_results_dir_c(self%sim_db_ptr, path_c_str%to_c_ptr())
    call c_f_pointer(c_str, f_str)
    unique_results_dir = f_str(1:index(f_str, c_null_char) - 1)
end function unique_results_dir

!> Get path to subdirectory in \p abs_path_to_dir unique to simulation.
!>
!> The subdirectory will be named 'date_time_name_id' and is intended to store
!> results in. If 'results_dir' in the database is empty, a new and unique
!> directory is created and the path stored in 'results_dir'. Otherwise the
!> path in 'results_dir' is just returned.
!>
!> @param abs_path_to_dir **character(len=*), intent(in)** Absolute path to 
!> where the new directory is created.
!> @return **character(len=:), allocatable** Path to new subdirectory.
function unique_results_dir_abs_path(self, abs_path_to_dir)
    class(sim_db)::self
    character(len=*), intent(in) :: abs_path_to_dir
    character(len=:), allocatable :: unique_results_dir_abs_path

    type(c_ptr) :: c_str
    character(len=huge(0), kind=c_char), pointer :: f_str
    type(c_string) :: path_c_str
    path_c_str = c_string(abs_path_to_dir)

    c_str = sim_db_unique_results_dir_abs_path_c(self%sim_db_ptr, &
                                                 path_c_str%to_c_ptr())
    call c_f_pointer(c_str, f_str)
    unique_results_dir_abs_path = f_str(1:index(f_str, c_null_char) - 1)
end function unique_results_dir_abs_path

!> Return true if \p column is a column in the database.
!>
!> @param column **character(len=*), intent(in)** Name of column in database.
function column_exists(self, column)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    logical :: column_exists

    type(c_string) :: column_c_str
    column_c_str = c_string(column)
    column_exists = logical(sim_db_column_exists_c(self%sim_db_ptr, &
                                                   column_c_str%to_c_ptr()))
end function column_exists

!> Return true if entry in database under \p column is empty.
!>
!> @param column **character(len=*), intent(in)** Name of column in database.
function is_empty(self, column)
    class(sim_db) :: self
    character(len=*), intent(in) :: column
    logical :: is_empty

    type(c_string) :: column_c_str
    column_c_str = c_string(column)
    is_empty = sim_db_is_empty_c(self%sim_db_ptr, column_c_str%to_c_ptr())
end function is_empty

!> Set entry under \p column in database to empty.
!>
!> @param column **character(len=*), intent(in)** Name of column in database.
subroutine set_empty(self, column)
    class(sim_db) :: self
    character(len=*), intent(in) :: column

    type(c_string) :: column_c_str
    column_c_str = c_string(column)
    call sim_db_set_empty_c(self%sim_db_ptr, column_c_str%to_c_ptr())
end subroutine set_empty

!> Return ID number of simulation in the database that is connected.
function get_id(self) result(id)
    class(sim_db) :: self
    integer :: id
    id = int(sim_db_get_id_c(self%sim_db_ptr))
end function get_id

!> Return path to root directory of the project, where *.sim_db/* is
!> located.
function get_path_proj_root(self) result(path_proj_root)
    class(sim_db) :: self
    character(len=:), allocatable :: path_proj_root

    type(c_ptr) :: c_str
    character(len=huge(0)), pointer :: f_str
    c_str = sim_db_get_path_proj_root_c(self%sim_db_ptr)
    call c_f_pointer(c_str, f_str)
    path_proj_root = f_str(1:index(f_str, c_null_char) - 1)
end function get_path_proj_root

!> @param paths_executables **character(len=:), dimension(:), allocatable, 
!> intent(in)** Paths to executable files.
!> @param len Length of \p paths_executables.
!> @param **logical, intent(in)** only_if_empty If True, it will only write to 
!> the database if the simulation's entry under 'sha1_executables' is empty. 
!> Will avoid any potential timeouts for concurrect applications.
subroutine update_sha1_executables_conditionally(self, paths_executables, &
                                                 only_if_empty)
    class(sim_db) :: self
    character(len=:), dimension(:), allocatable, intent(in) :: paths_executables
    logical, intent(in) :: only_if_empty

    type(c_ptr), dimension(:), allocatable, target :: c_ptr_array
    integer :: i
    type(c_string) :: c_str

    allocate(c_ptr_array(size(paths_executables)))
    do i = 1, size(paths_executables)
        c_str = c_string(paths_executables(i))
        c_ptr_array(i) = c_str%to_c_ptr()
    end do

    call sim_db_update_sha1_executables_c(self%sim_db_ptr, c_ptr_array, &
        int(size(c_ptr_array), kind=c_size_t), &
        logical(only_if_empty, kind=c_bool)) 
end subroutine update_sha1_executables_conditionally

!> @param paths_executables **character(len=:), dimension(:), allocatable, 
!> intent(in)** Paths to executable files.
!> @param len Length of \p paths_executables.
subroutine update_sha1_executables_unconditionally(self, paths_executables)
    class(sim_db) :: self
    character(len=:), dimension(:), allocatable, intent(in) :: paths_executables
    call update_sha1_executables_conditionally(self, paths_executables, .false.) 
end subroutine update_sha1_executables_unconditionally

!> Allow timeouts to occure without exiting if set to true.
!>
!> A timeout occures after waiting more than 5 seconds to access the database
!> because other threads/processes are busy writing to it. **sim_db**
!> will exit with an error in that case, unless allow timeouts is set to true.
!> It is false by default. If allowed and a timeout occures the called
!> funciton will have had no effect.
subroutine allow_timeouts(self, is_allowing_timeouts)
    class(sim_db) :: self
    logical, intent(in) :: is_allowing_timeouts
    call sim_db_allow_timeouts_c(self%sim_db_ptr, &
                                 logical(is_allowing_timeouts, kind=c_bool))
end subroutine allow_timeouts

!> Checks if a timeout have occured since last call to this function.
function have_timed_out(self) 
    class(sim_db) :: self
    logical :: have_timed_out
    have_timed_out = logical(sim_db_have_timed_out_c(self%sim_db_ptr))
end function have_timed_out

!> Delete simulation from database.
subroutine delete_from_database(self)
    class(sim_db) :: self
    call sim_db_delete_from_database_c(self%sim_db_ptr)
end subroutine delete_from_database

!> Add metadate for 'used_walltime' to database and update 'status' to
!> 'finished' and cleans up.
subroutine close(self)
    class(sim_db) :: self
    call sim_db_dtor_c(self%sim_db_ptr)
end subroutine close

subroutine sim_db_dtor(self)
    type(sim_db) :: self
    call sim_db_dtor_c(self%sim_db_ptr)
end subroutine sim_db_dtor

type(sim_db) function sim_db_add_empty_sim_with_search(store_metadata)
    logical, optional, value :: store_metadata

    type(c_ptr) :: empty_sim_db
    if (.not. present(store_metadata)) store_metadata = .false.

    empty_sim_db = sim_db_add_empty_sim_c(logical(store_metadata, kind=c_bool))
    sim_db_add_empty_sim_with_search%sim_db_ptr = empty_sim_db
end function sim_db_add_empty_sim_with_search

!> Add empty simulation to database and return a type(sim_db) connected to it.
!>
!> The current working directory and its parent directories will be searched
!> until *.sim_db/* is found.
!>
!> @return **type(sim_db)** of the added simulation.
!> @param store_metadata **logical** Stores metadata if true. Set to 'false' for
!> postprocessing (e.g. visualization) of data from simulation.
type(sim_db) function sim_db_add_empty_sim_without_search(path_proj_root, &
                                                      store_metadata)
    character(len=*), intent(in) :: path_proj_root
    logical, value :: store_metadata

    type(c_string) :: path_proj_root_c_str
    type(c_ptr) :: empty_sim_db

    path_proj_root_c_str = c_string(path_proj_root)
    empty_sim_db = sim_db_add_empty_sim_without_search_c( &
        path_proj_root_c_str%to_c_ptr(), logical(store_metadata, kind=c_bool))
    sim_db_add_empty_sim_without_search%sim_db_ptr = empty_sim_db
end function sim_db_add_empty_sim_without_search

!> Add empty simulation to database and return a type(sim_db) connected to it.
!>
!> The current working directory and its parent directories will be searched
!> until *.sim_db/* is found.
!>
!> @return **type(sim_db)** of the added simulation.
!> @param path_proj_root **character(len=*), intent(in)** Path to root 
!> directory of the project, where *.sim_db/* is located.
!> @param store_metadata **logical** Stores metadata if true. Set to 'false' for
!> postprocessing (e.g. visualization) of data from simulation.
type(sim_db) function sim_db_add_empty_sim_without_search_false(path_proj_root)
    character(len=*), intent(in) :: path_proj_root
    sim_db_add_empty_sim_without_search_false = &
        sim_db_add_empty_sim_without_search(path_proj_root, .false.)
end function sim_db_add_empty_sim_without_search_false

type(c_string) function c_string_ctor(f_string) result(obj)
    character(len=*), intent(in) :: f_string

    integer :: len_str
    len_str = len_trim(f_string)
    allocate(character(len_str + 1) :: obj%c_str)
    obj%c_str = f_string
    obj%c_str(len_str + 1:len_str + 1) = c_null_char
end function c_string_ctor

type(c_ptr) function to_c_ptr(self)
    class(c_string) :: self
    to_c_ptr = c_loc(self%c_str)
end function to_c_ptr

subroutine c_string_dtor(self)
    type(c_string) :: self
    deallocate(self%c_str)
end subroutine c_string_dtor

end module sim_db_mod !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
