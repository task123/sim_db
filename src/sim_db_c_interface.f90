module sim_db_c_interface
use, intrinsic :: iso_c_binding, only : c_size_t, c_ptr

type, bind(c) :: sim_db_vec
    integer(c_size_t) :: size
    type(c_ptr) :: array
end type sim_db_vec

interface ! Interface to sim_db C functions

    type(c_ptr) function sim_db_ctor_c(argc, argv) &
            bind(c, name="sim_db_ctor")
        use, intrinsic :: iso_c_binding, only : c_int, c_ptr
        implicit none
        integer(c_int), value, intent(in) :: argc
        type(c_ptr), value, intent(in) :: argv
    end function sim_db_ctor_c

    type(c_ptr) function sim_db_ctor_no_metadata_c(argc, argv) &
            bind(c, name="sim_db_ctor_no_metadata")
        use, intrinsic :: iso_c_binding, only : c_int, c_ptr
        implicit none
        integer(c_int), value, intent(in) :: argc
        type(c_ptr), value, intent(in) :: argv
    end function sim_db_ctor_no_metadata_c

    type(c_ptr) function sim_db_ctor_with_id_c(id, store_metadata) &
            bind(c, name="sim_db_ctor_with_id")
        use, intrinsic :: iso_c_binding, only : c_int, c_bool, c_ptr
        implicit none
        integer(c_int), value, intent(in) :: id
        logical(c_bool), value, intent(in) :: store_metadata
    end function sim_db_ctor_with_id_c

    type(c_ptr) function sim_db_ctor_without_search_c(path_proj_root, id, &
            store_metadata) bind(c, name="sim_db_ctor_without_search")
        use, intrinsic :: iso_c_binding, only : c_int, c_bool, c_ptr
        implicit none
        type(c_ptr), value, intent(in) :: path_proj_root
        integer(c_int), value, intent(in) :: id
        logical(c_bool), value, intent(in) :: store_metadata
    end function sim_db_ctor_without_search_c

    integer(c_int) function sim_db_read_int_c(sim_db_ptr, column) &
            bind(c, name="sim_db_read_int")
        use, intrinsic :: iso_c_binding, only : c_ptr, c_int
        implicit none
        type(c_ptr), value, intent(in) :: sim_db_ptr
        type(c_ptr), value, intent(in) :: column
    end function sim_db_read_int_c

    real(c_double) function sim_db_read_double_c(sim_db_ptr, column) &
            bind(c, name="sim_db_read_double")
        use, intrinsic :: iso_c_binding, only : c_ptr, c_double
        implicit none
        type(c_ptr), value, intent(in) :: sim_db_ptr
        type(c_ptr), value, intent(in) :: column
    end function sim_db_read_double_c

    type(c_ptr) function sim_db_read_string_c(sim_db_ptr, column) &
            bind(c, name="sim_db_read_string")
        use, intrinsic :: iso_c_binding, only : c_ptr
        implicit none
        type(c_ptr), value, intent(in) :: sim_db_ptr
        type(c_ptr), value, intent(in) :: column
    end function sim_db_read_string_c

    logical(kind=c_bool) function sim_db_read_bool_c(sim_db_ptr, column) &
            bind(c, name="sim_db_read_bool")
        use, intrinsic :: iso_c_binding, only : c_ptr, c_bool
        implicit none
        type(c_ptr), value, intent(in) :: sim_db_ptr
        type(c_ptr), value, intent(in) :: column
    end function sim_db_read_bool_c

    type(sim_db_vec) function sim_db_read_int_vec_c(sim_db_ptr, column) &
            bind(c, name="sim_db_read_int_vec")
        use, intrinsic :: iso_c_binding, only : c_ptr, c_size_t
        implicit none
        type, bind(c) :: sim_db_vec
            integer(c_size_t) :: size
            type(c_ptr) :: array
        end type sim_db_vec
        type(c_ptr), value, intent(in) :: sim_db_ptr
        type(c_ptr), value, intent(in) :: column
    end function sim_db_read_int_vec_c

    type(sim_db_vec) function sim_db_read_double_vec_c(sim_db_ptr, column) &
            bind(c, name="sim_db_read_double_vec")
        use, intrinsic :: iso_c_binding, only : c_ptr, c_size_t
        implicit none
        type, bind(c) :: sim_db_vec
            integer(c_size_t) :: size
            type(c_ptr) :: array
        end type sim_db_vec
        type(c_ptr), value, intent(in) :: sim_db_ptr
        type(c_ptr), value, intent(in) :: column
    end function sim_db_read_double_vec_c

    type(sim_db_vec) function sim_db_read_string_vec_c(sim_db_ptr, column) &
            bind(c, name="sim_db_read_string_vec")
        use, intrinsic :: iso_c_binding, only : c_ptr, c_size_t
        implicit none
        type, bind(c) :: sim_db_vec
            integer(c_size_t) :: size
            type(c_ptr) :: array
        end type sim_db_vec
        type(c_ptr), value, intent(in) :: sim_db_ptr
        type(c_ptr), value, intent(in) :: column
    end function sim_db_read_string_vec_c

    type(sim_db_vec) function sim_db_read_bool_vec_c(sim_db_ptr, column) &
            bind(c, name="sim_db_read_bool_vec")
        use, intrinsic :: iso_c_binding, only : c_ptr, c_size_t
        implicit none
        type, bind(c) :: sim_db_vec
            integer(c_size_t) :: size
            type(c_ptr) :: array
        end type sim_db_vec
        type(c_ptr), value, intent(in) :: sim_db_ptr
        type(c_ptr), value, intent(in) :: column
    end function sim_db_read_bool_vec_c

    subroutine sim_db_write_int_c(sim_db_ptr, column, int_value, only_if_empty) &
            bind(c, name="sim_db_write_int")
        use, intrinsic :: iso_c_binding, only : c_ptr, c_int, c_bool
        implicit none
        type(c_ptr), value, intent(in) :: sim_db_ptr
        type(c_ptr), value, intent(in) :: column
        integer(c_int), value, intent(in) :: int_value
        logical(c_bool), value, intent(in) :: only_if_empty
    end subroutine sim_db_write_int_c

    subroutine sim_db_write_double_c(sim_db_ptr, column, real_value, only_if_empty) &
            bind(c, name="sim_db_write_double")
        use, intrinsic :: iso_c_binding, only : c_ptr, c_double, c_bool
        implicit none
        type(c_ptr), value, intent(in) :: sim_db_ptr
        type(c_ptr), value, intent(in) :: column
        real(c_double), value, intent(in) :: real_value
        logical(c_bool), value, intent(in) :: only_if_empty
    end subroutine sim_db_write_double_c

    subroutine sim_db_write_string_c(sim_db_ptr, column, string_value, only_if_empty) &
            bind(c, name="sim_db_write_string")
        use, intrinsic :: iso_c_binding, only : c_ptr, c_bool
        implicit none
        type(c_ptr), value, intent(in) :: sim_db_ptr
        type(c_ptr), value, intent(in) :: column
        type(c_ptr), value, intent(in) :: string_value
        logical(c_bool), value, intent(in) :: only_if_empty
    end subroutine sim_db_write_string_c

    subroutine sim_db_write_bool_c(sim_db_ptr, column, bool_value, only_if_empty) &
            bind(c, name="sim_db_write_bool")
        use, intrinsic :: iso_c_binding, only : c_ptr, c_bool
        implicit none
        type(c_ptr), value, intent(in) :: sim_db_ptr
        type(c_ptr), value, intent(in) :: column
        logical(c_bool), value, intent(in) :: bool_value
        logical(c_bool), value, intent(in) :: only_if_empty
    end subroutine sim_db_write_bool_c

    subroutine sim_db_write_int_array_c(sim_db_ptr, column, int_array, length, &
            only_if_empty) bind(c, name="sim_db_write_int_array")
        use, intrinsic :: iso_c_binding, only : c_ptr, c_int, c_bool
        implicit none
        type(c_ptr), value, intent(in) :: sim_db_ptr
        type(c_ptr), value, intent(in) :: column
        type(c_ptr), value, intent(in) :: int_array
        integer(c_int), value, intent(in) :: length
        logical(c_bool), value, intent(in) :: only_if_empty
    end subroutine sim_db_write_int_array_c

    subroutine sim_db_write_double_array_c(sim_db_ptr, column, real_array, &
            length, only_if_empty) bind(c, name="sim_db_write_double_array")
        use, intrinsic :: iso_c_binding, only : c_ptr, c_int, c_bool
        implicit none
        type(c_ptr), value, intent(in) :: sim_db_ptr
        type(c_ptr), value, intent(in) :: column
        type(c_ptr), value, intent(in) :: real_array
        integer(c_int), value, intent(in) :: length
        logical(c_bool), value, intent(in) :: only_if_empty
    end subroutine sim_db_write_double_array_c

    subroutine sim_db_write_string_array_c(sim_db_ptr, column, string_array, &
            length, only_if_empty) bind(c, name="sim_db_write_string_array")
        use, intrinsic :: iso_c_binding, only : c_ptr, c_int, c_bool
        implicit none
        type(c_ptr), value, intent(in) :: sim_db_ptr
        type(c_ptr), value, intent(in) :: column
        type(c_ptr), value, intent(in) :: string_array
        integer(c_int), value, intent(in) :: length
        logical(c_bool), value, intent(in) :: only_if_empty
    end subroutine sim_db_write_string_array_c

    subroutine sim_db_write_bool_array_c(sim_db_ptr, column, bool_array, &
            length, only_if_empty) bind(c, name="sim_db_write_bool_array")
        use, intrinsic :: iso_c_binding, only : c_ptr, c_int, c_bool
        implicit none
        type(c_ptr), value, intent(in) :: sim_db_ptr
        type(c_ptr), value, intent(in) :: column
        type(c_ptr), value, intent(in) :: bool_array
        integer(c_int), value, intent(in) :: length
        logical(c_bool), value, intent(in) :: only_if_empty
    end subroutine sim_db_write_bool_array_c

    type(c_ptr) function sim_db_unique_results_dir_c(sim_db_ptr, path_to_dir) &
            bind(c, name="sim_db_unique_results_dir")
        use, intrinsic :: iso_c_binding, only : c_ptr
        implicit none
        type(c_ptr), value, intent(in) :: sim_db_ptr
        type(c_ptr), value, intent(in) :: path_to_dir
    end function sim_db_unique_results_dir_c

    type(c_ptr) function sim_db_unique_results_dir_abs_path_c(sim_db_ptr, &
            abs_path_to_dir) bind(c, name="sim_db_unique_results_dir")
        use, intrinsic :: iso_c_binding, only : c_ptr
        implicit none
        type(c_ptr), value, intent(in) :: sim_db_ptr
        type(c_ptr), value, intent(in) :: abs_path_to_dir
    end function sim_db_unique_results_dir_abs_path_c

   logical(c_bool) function sim_db_column_exists_c(sim_db_ptr, column) &
            bind(c, name="sim_db_column_exists")
        use, intrinsic :: iso_c_binding, only : c_ptr, c_bool
        implicit none
        type(c_ptr), value, intent(in) :: sim_db_ptr
        type(c_ptr), value, intent(in) :: column
    end function sim_db_column_exists_c

    logical(c_bool) function sim_db_is_empty_c(sim_db_ptr, column) &
            bind(c, name="sim_db_is_empty")
        use, intrinsic :: iso_c_binding, only : c_ptr, c_bool
        implicit none
        type(c_ptr), value, intent(in) :: sim_db_ptr
        type(c_ptr), value, intent(in) :: column
    end function sim_db_is_empty_c

    subroutine sim_db_set_empty_c(sim_db_ptr, column) &
            bind(c, name="sim_db_set_empty")
        use, intrinsic :: iso_c_binding, only : c_ptr
        implicit none
        type(c_ptr), value, intent(in) :: sim_db_ptr
        type(c_ptr), value, intent(in) :: column
    end subroutine sim_db_set_empty_c

    integer(c_int) function sim_db_get_id_c(sim_db_ptr) &
            bind(c, name="sim_db_get_id")
        use, intrinsic :: iso_c_binding, only : c_ptr, c_int
        implicit none
        type(c_ptr), value, intent(in) :: sim_db_ptr
    end function sim_db_get_id_c

    type(c_ptr) function sim_db_get_path_proj_root_c(sim_db_ptr) &
            bind(c, name="sim_db_get_path_proj_root")
        use, intrinsic :: iso_c_binding, only : c_ptr
        implicit none
        type(c_ptr), value, intent(in) :: sim_db_ptr
    end function sim_db_get_path_proj_root_c

    subroutine sim_db_update_sha1_executables_c(sim_db_ptr, paths_executables, &
            length, only_if_empty) &
            bind(c, name="sim_db_update_sha1_executables")
        use, intrinsic :: iso_c_binding, only : c_ptr, c_bool, c_size_t
        implicit none
        type(c_ptr), value, intent(in) :: sim_db_ptr
        type(c_ptr), value, intent(in) :: paths_executables
        integer(c_size_t), value, intent(in) :: length
        logical(c_bool), value, intent(in) :: only_if_empty
    end subroutine sim_db_update_sha1_executables_c

    subroutine sim_db_allow_timeouts_c(sim_db_ptr, allow_timeouts) &
            bind(c, name="sim_db_allow_timeouts")
        use, intrinsic :: iso_c_binding, only : c_ptr, c_bool
        implicit none
        type(c_ptr), value, intent(in) :: sim_db_ptr
        logical(c_bool), value, intent(in) :: allow_timeouts
    end subroutine sim_db_allow_timeouts_c

    logical(c_bool) function sim_db_have_timed_out_c(sim_db_ptr) &
            bind(c, name="sim_db_have_timed_out")
        use, intrinsic :: iso_c_binding, only : c_ptr, c_bool
        implicit none
        type(c_ptr), value, intent(in) :: sim_db_ptr
    end function sim_db_have_timed_out_c

    subroutine sim_db_delete_from_database_c(sim_db_ptr) &
            bind(c, name="sim_db_delete_from_database")
        use, intrinsic :: iso_c_binding, only : c_ptr
        implicit none
        type(c_ptr), value, intent(in) :: sim_db_ptr
    end subroutine sim_db_delete_from_database_c

    subroutine sim_db_dtor_c(sim_db_ptr) bind(c, name="sim_db_dtor")
        use, intrinsic :: iso_c_binding, only : c_ptr
        implicit none
        type(c_ptr), value, intent(in) :: sim_db_ptr
    end subroutine

    type(c_ptr) function sim_db_add_emtpy_sim(store_metadata)
        use, intrinsic :: iso_c_binding, only : c_ptr, c_bool
        implicit none
        logical(c_bool), value, intent(in) :: store_metadata
    end function

    type(c_ptr) function sim_db_add_emtpy_sim_without_search(path_proj_root, &
            store_metadata)
        use, intrinsic :: iso_c_binding, only : c_ptr, c_bool
        implicit none
        type(c_ptr), value, intent(in) :: path_proj_root
        logical(c_bool), value, intent(in) :: store_metadata
    end function

end interface ! Interface to sim_db C functions

end module sim_db_c_interface
