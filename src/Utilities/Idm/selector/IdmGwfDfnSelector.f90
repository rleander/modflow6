! ** Do Not Modify! MODFLOW 6 system generated file. **
module IdmGwfDfnSelectorModule

  use SimModule, only: store_error
  use InputDefinitionModule, only: InputParamDefinitionType, &
                                   InputBlockDefinitionType
  use GwfDisInputModule, only: gwf_dis_param_definitions, &
                               gwf_dis_aggregate_definitions, &
                               gwf_dis_block_definitions, &
                               gwf_dis_multi_package
  use GwfDisuInputModule, only: gwf_disu_param_definitions, &
                                gwf_disu_aggregate_definitions, &
                                gwf_disu_block_definitions, &
                                gwf_disu_multi_package
  use GwfDisvInputModule, only: gwf_disv_param_definitions, &
                                gwf_disv_aggregate_definitions, &
                                gwf_disv_block_definitions, &
                                gwf_disv_multi_package
  use GwfNpfInputModule, only: gwf_npf_param_definitions, &
                               gwf_npf_aggregate_definitions, &
                               gwf_npf_block_definitions, &
                               gwf_npf_multi_package
  use GwfNamInputModule, only: gwf_nam_param_definitions, &
                               gwf_nam_aggregate_definitions, &
                               gwf_nam_block_definitions, &
                               gwf_nam_multi_package

  implicit none
  private
  public :: gwf_param_definitions
  public :: gwf_aggregate_definitions
  public :: gwf_block_definitions
  public :: gwf_idm_multi_package
  public :: gwf_idm_integrated

contains

  subroutine set_param_pointer(input_dfn, input_dfn_target)
    type(InputParamDefinitionType), dimension(:), pointer :: input_dfn
    type(InputParamDefinitionType), dimension(:), target :: input_dfn_target
    input_dfn => input_dfn_target
  end subroutine set_param_pointer

  subroutine set_block_pointer(input_dfn, input_dfn_target)
    type(InputBlockDefinitionType), dimension(:), pointer :: input_dfn
    type(InputBlockDefinitionType), dimension(:), target :: input_dfn_target
    input_dfn => input_dfn_target
  end subroutine set_block_pointer

  function gwf_param_definitions(subcomponent) result(input_definition)
    character(len=*), intent(in) :: subcomponent
    type(InputParamDefinitionType), dimension(:), pointer :: input_definition
    nullify (input_definition)
    select case (subcomponent)
    case ('DIS')
      call set_param_pointer(input_definition, gwf_dis_param_definitions)
    case ('DISU')
      call set_param_pointer(input_definition, gwf_disu_param_definitions)
    case ('DISV')
      call set_param_pointer(input_definition, gwf_disv_param_definitions)
    case ('NPF')
      call set_param_pointer(input_definition, gwf_npf_param_definitions)
    case ('NAM')
      call set_param_pointer(input_definition, gwf_nam_param_definitions)
    case default
    end select
    return
  end function gwf_param_definitions

  function gwf_aggregate_definitions(subcomponent) result(input_definition)
    character(len=*), intent(in) :: subcomponent
    type(InputParamDefinitionType), dimension(:), pointer :: input_definition
    nullify (input_definition)
    select case (subcomponent)
    case ('DIS')
      call set_param_pointer(input_definition, gwf_dis_aggregate_definitions)
    case ('DISU')
      call set_param_pointer(input_definition, gwf_disu_aggregate_definitions)
    case ('DISV')
      call set_param_pointer(input_definition, gwf_disv_aggregate_definitions)
    case ('NPF')
      call set_param_pointer(input_definition, gwf_npf_aggregate_definitions)
    case ('NAM')
      call set_param_pointer(input_definition, gwf_nam_aggregate_definitions)
    case default
    end select
    return
  end function gwf_aggregate_definitions

  function gwf_block_definitions(subcomponent) result(input_definition)
    character(len=*), intent(in) :: subcomponent
    type(InputBlockDefinitionType), dimension(:), pointer :: input_definition
    nullify (input_definition)
    select case (subcomponent)
    case ('DIS')
      call set_block_pointer(input_definition, gwf_dis_block_definitions)
    case ('DISU')
      call set_block_pointer(input_definition, gwf_disu_block_definitions)
    case ('DISV')
      call set_block_pointer(input_definition, gwf_disv_block_definitions)
    case ('NPF')
      call set_block_pointer(input_definition, gwf_npf_block_definitions)
    case ('NAM')
      call set_block_pointer(input_definition, gwf_nam_block_definitions)
    case default
    end select
    return
  end function gwf_block_definitions

  function gwf_idm_multi_package(subcomponent) result(multi_package)
    character(len=*), intent(in) :: subcomponent
    logical :: multi_package
    select case (subcomponent)
    case ('DIS')
      multi_package = gwf_dis_multi_package
    case ('DISU')
      multi_package = gwf_disu_multi_package
    case ('DISV')
      multi_package = gwf_disv_multi_package
    case ('NPF')
      multi_package = gwf_npf_multi_package
    case ('NAM')
      multi_package = gwf_nam_multi_package
    case default
      call store_error('Idm selector subcomponent not found; '//&
                       &'component="GWF"'//&
                       &', subcomponent="'//trim(subcomponent)//'".', .true.)
    end select
    return
  end function gwf_idm_multi_package

  function gwf_idm_integrated(subcomponent) result(integrated)
    character(len=*), intent(in) :: subcomponent
    logical :: integrated
    integrated = .false.
    select case (subcomponent)
    case ('DIS')
      integrated = .true.
    case ('DISU')
      integrated = .true.
    case ('DISV')
      integrated = .true.
    case ('NPF')
      integrated = .true.
    case ('NAM')
      integrated = .true.
    case default
    end select
    return
  end function gwf_idm_integrated

end module IdmGwfDfnSelectorModule
