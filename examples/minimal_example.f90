! Minimal example showing how to use the Fortran verions of 'sim_db'.
!
! Usage: 'add_and_run --filename params_minimal_fortran_example.txt'
!    or with parameters with id, ID, in database:
!        'make minimal_fortran_example_updated'
!      + './minimal_fortran_example --id ID --path_sim_db ".."

! Copyright (C) 2019 Håkon Austlid Taskén <hakon.tasken@gmail.com>
! Licensed under the MIT License.

program minimal_example
    use sim_db_mod
    implicit none

    type(sim_db) :: sim_database
    character(len=:), allocatable :: param1
    integer :: param2

    ! Open database and write some initial metadata to database.
    sim_database = sim_db()

    ! Read parameters from database.
    call sim_database%read("param1", param1)
    call sim_database%read("param2", param2)

    ! Demonstrate that the simulation is running.
    print *, param1
end program minimal_example
