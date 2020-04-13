! Testing 'sim_db' for Fortran, that is 'sim_db_mod.f90' and 
! 'sim_db_c_interface.f90'.
!
! Read in parameters from database, write parameters to database, make unique
! subdirectory for results and save 'results.txt' in this directory.

! Copyright (C) 2019 Håkon Austlid Taskén <hakon.tasken@gmail.com>
! Licensed under the MIT License.

module print_adjust
implicit none

    interface print_left_adjusted
        module procedure print_left_adjusted_int, print_left_adjusted_real, &
             print_left_adjusted_string, print_left_adjusted_logical
    end interface print_left_adjusted

contains

    subroutine print_string(string)
        character(len=*) :: string
        write(*,'(a)') string
    end subroutine print_string

    subroutine print_left_adjusted_string(string)
        character(len=*) :: string
        call print_string(trim(adjustl(string)))
    end subroutine print_left_adjusted_string

    subroutine print_left_adjusted_int(int_value)
        integer :: int_value

        character(len=100) :: string
        write(string,*) int_value
        call print_string(trim(adjustl(string)))
    end subroutine print_left_adjusted_int

    subroutine print_left_adjusted_real(real_value)
        real :: real_value

        character(len=100) :: string
        write(string,*) real_value
        call print_string(trim(adjustl(string)))
    end subroutine print_left_adjusted_real

    subroutine print_left_adjusted_logical(logical_value)
        logical :: logical_value

        integer :: bool
        bool = 0
        if (logical_value) then 
            bool = 1
        end if 
        call print_left_adjusted_int(bool)
    end subroutine print_left_adjusted_logical
end module print_adjust

program main
    use sim_db_mod
    use print_adjust
    implicit none


type(sim_db) :: sim_database, sim_database_2
logical :: store_metadata
character(len=100) :: command_line_argument
integer :: i, nargs, len_str, param1, new_param1, param9, new_param9
integer :: param10, new_param10
real :: param2, new_param2
character(len=:), allocatable :: param3, new_param3, path_proj_root
character(len=1000) :: filename_result
logical :: param4, new_param4
integer, dimension(:), allocatable :: param5, new_param5
real, dimension(:), allocatable :: param6, new_param6
character(len=:), dimension(:), allocatable :: param7, new_param7
logical, dimension(:), allocatable :: param8, new_param8

store_metadata = .true.

nargs = command_argument_count()
do i = 1, nargs
    call get_command_argument(i, command_line_argument)
    len_str = len_trim(command_line_argument)
    if (len_str >= 100) then
        error stop "ERROR: Command line argument longer than the maximum &
                   &100 characters."
    end if
    if (command_line_argument == "no_metadata") then
        store_metadata = .false.
    end if
end do

sim_database = sim_db(store_metadata)

call sim_database%read("test_param1", param1)
call print_left_adjusted(param1)
call sim_database%write("new_test_param1", param1)
call sim_database%read("new_test_param1", new_param1)
call print_left_adjusted(new_param1)

call sim_database%read("test_param2", param2)
call print_left_adjusted(param2)
call sim_database%write("new_test_param2", param2)
call sim_database%read("new_test_param2", new_param2)
call print_left_adjusted(new_param2)

call sim_database%read("test_param3", param3)
call print_left_adjusted(param3)
call sim_database%write("new_test_param3", param3)
call sim_database%read("new_test_param3", new_param3)
call print_left_adjusted(new_param3)

call sim_database%read("test_param4", param4)
call print_left_adjusted(param4)
call sim_database%write("new_test_param4", param4)
call sim_database%read("new_test_param4", new_param4)
call print_left_adjusted(new_param4)

call sim_database%read("test_param5", param5)
do i = 1, size(param5)
    call print_left_adjusted(param5(i))
end do
call sim_database%write("new_test_param5", param5)
call sim_database%read("new_test_param5", new_param5)
do i = 1, size(new_param5)
    call print_left_adjusted(new_param5(i))
end do

call sim_database%read("test_param6", param6)
do i = 1, size(param6)
    call print_left_adjusted(param6(i))
end do
call sim_database%write("new_test_param6", param6)
call sim_database%read("new_test_param6", new_param6)
do i = 1, size(new_param6)
    call print_left_adjusted(new_param6(i))
end do

call sim_database%read("test_param7", param7)
do i = 1, size(param7)
    call print_left_adjusted(param7(i))
end do
call sim_database%write("new_test_param7", param7)
call sim_database%read("new_test_param7", new_param7)
do i = 1, size(new_param7)
    call print_left_adjusted(new_param7(i))
end do

call sim_database%read("test_param8", param8)
do i = 1, size(param8)
    call print_left_adjusted(param8(i))
end do
call sim_database%write("new_test_param8", param8)
call sim_database%read("new_test_param8", new_param8)
do i = 1, size(new_param8)
    call print_left_adjusted(new_param8(i))
end do

call sim_database%read("test_param9", param9)
call print_left_adjusted(param9)
call sim_database%write("new_test_param9", param9)
call sim_database%read("new_test_param9", new_param9)
call print_left_adjusted(new_param9)

call sim_database%read("test_param10", param10)
call print_left_adjusted(param10)
call sim_database%write("new_test_param10", param10)
call sim_database%read("new_test_param10", new_param10)
call print_left_adjusted(new_param10)

call print_left_adjusted(sim_database%is_empty("test_param11"))
call sim_database%set_empty("test_param11")
call print_left_adjusted(sim_database%is_empty("test_param11"))

if (store_metadata) then
    ! Make unique subdirector in results/.
    filename_result = &
        sim_database%unique_results_dir("root/tests/results/") &
        // "/results.txt"

    ! Save param6 to file in this unique subdirectory.
    open(1, file=filename_result, status="new")
    write(1,*) param6
    close(1)
end if

call print_left_adjusted(sim_database%column_exists("test_param1"))
call print_left_adjusted(sim_database%column_exists("test_column_does_not_exists"))

path_proj_root = sim_database%get_path_proj_root()

call sim_database%close()

sim_database_2 = sim_db_add_empty_sim(.false.)
call print_left_adjusted(sim_database_2%get_id())

call sim_database_2%write("test_param1", 7)
call sim_database_2%read("test_param1", param1)
call print_left_adjusted(param1)

call sim_database_2%delete_from_database()

call sim_database_2%close()

end program main

