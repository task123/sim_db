! Extensive example showing how to use the Fortran verions of 'sim_db'.
!
! Usage: 'add_and_run --filename params_extensive_fortran_example.txt'
!    or with parameters with id, ID, in database:
!        'make extensive_fortran_example_updated'
!      + './extensive_fortran_example --id ID --path_sim_db ".."

! Copyright (C) 2019 Håkon Austlid Taskén <hakon.tasken@gmail.com>
! Licensed under the MIT License.

program extensive_example
    use class_sim_db
    implicit none
    
    type(sim_db) :: sim_database, sim_database_2
    integer :: param1, i, id
    real :: param2
    real(kind=kind(1.0d0)) :: param2_dp
    character(len=:), allocatable :: param3, name_results_dir, path_proj_root
    logical :: param4, is_column_in_database, is_empty
    integer, dimension(:), allocatable :: param5
    real, dimension(:), allocatable :: param6
    real(kind=kind(1.0d0)), dimension(:), allocatable :: param6_dp
    character(len=:), dimension(:), allocatable :: param7
    logical, dimension(:), allocatable :: param8

    ! Open database and write some inital metadata to database.
    sim_database = sim_db()

    ! Read parameters from database.
    call sim_database%read("param1_extensive", param1)
    call sim_database%read("param2_extensive", param2)
    call sim_database%read("param2_extensive", param2_dp)
    call sim_database%read("param3_extensive", param3)
    call sim_database%read("param4_extensive", param4)
    call sim_database%read("param5_extensive", param5)
    call sim_database%read("param6_extensive", param6)
    call sim_database%read("param6_extensive", param6_dp)
    call sim_database%read_string_array("param7_extensive", param7)
    call sim_database%read("param8_extensive", param8)

    ! Demostrate that the simulation is running.
    print *, param3

    ! Write all the possible types to database.
    ! Only these types are can be written to the database.
    call sim_database%write("example_result_1", param1)
    call sim_database%write("example_result_2", param2)
    call sim_database%write("example_result_2", param2_dp)
    call sim_database%write("example_result_3", param3)
    call sim_database%write("example_result_4", param4)
    call sim_database%write("example_result_5", param5)
    call sim_database%write("example_result_6", param6)
    call sim_database%write("example_result_6", param6_dp)
    call sim_database%write("example_result_7", param7)
    call sim_database%write("example_result_8", param8)


    ! Make unique subdirectory for storing results and write its name to
    ! database. Large results are recommended to be saved in this subdirectory.
    name_results_dir = sim_database%unique_results_dir("root/examples/results")

    ! Write some results to a file in the newly create subdirectory.
    open(1, file=name_results_dir // "/results.txt")
    do i = 1, size(param6)
        write (1,*) param6(i) 
    end do

    ! Check if column exists in database.
    is_column_in_database = sim_database%column_exists("column_not_in_database")

    ! Check if column is empty and then set it to empty.
    is_empty = sim_database%is_empty("example_results_1")
    call sim_database%set_empty("example_result_1")

    ! Get the 'ID' of the connected simulation an the path to the project's
    ! root directory.
    id = sim_database%get_id()
    path_proj_root = sim_database%get_path_proj_root()

    ! Add an empty simulation to the database, open connection and write to it.
    sim_database_2 = sim_db_add_empty_sim(path_proj_root);
    call sim_database_2%write("param1_extensive", 7)

    ! Delete simulation from database.
    call sim_database_2%delete_from_database()

    call sim_database % close()

end program extensive_example
