import os

import flopy
import numpy as np
import pytest
from framework import TestFramework
from simulation import TestSimulation

ex = ["tvk05"]
time_varying_k = [1.0, 10.0]


def build_model(idx, dir):
    nlay, nrow, ncol = 1, 3, 3
    perlen = [100.0, 100.0]
    nper = len(perlen)
    nstp = nper * [1]
    tsmult = nper * [1.0]
    delr = 1.0
    delc = 1.0
    delz = 1.0
    top = 1.0
    laytyp = 0
    botm = [0.0]
    strt = 1.0
    hk = 0.1

    nouter, ninner = 100, 300
    hclose, rclose, relax = 1e-6, 1e-6, 1.0

    tdis_rc = []
    for i in range(nper):
        tdis_rc.append((perlen[i], nstp[i], tsmult[i]))

    name = ex[idx]

    # build MODFLOW 6 files
    ws = dir
    sim = flopy.mf6.MFSimulation(
        sim_name=name, version="mf6", exe_name="mf6", sim_ws=ws
    )
    # create tdis package
    tdis = flopy.mf6.ModflowTdis(
        sim, time_units="DAYS", nper=nper, perioddata=tdis_rc
    )

    # create gwf model
    gwfname = "gwf_" + name
    gwf = flopy.mf6.MFModel(
        sim,
        model_type="gwf6",
        modelname=gwfname,
        model_nam_file=f"{gwfname}.nam",
    )
    gwf.name_file.save_flows = True

    # create iterative model solution and register the gwf model with it
    imsgwf = flopy.mf6.ModflowIms(
        sim,
        print_option="SUMMARY",
        outer_dvclose=hclose,
        outer_maximum=nouter,
        under_relaxation="NONE",
        inner_maximum=ninner,
        inner_dvclose=hclose,
        rcloserecord=rclose,
        linear_acceleration="CG",
        scaling_method="NONE",
        reordering_method="NONE",
        relaxation_factor=relax,
        filename=f"{gwfname}.ims",
    )
    sim.register_ims_package(imsgwf, [gwf.name])

    dis = flopy.mf6.ModflowGwfdis(
        gwf,
        nlay=nlay,
        nrow=nrow,
        ncol=ncol,
        delr=delr,
        delc=delc,
        top=top,
        botm=botm,
        idomain=np.ones((nlay, nrow, ncol), dtype=int),
        filename=f"{gwfname}.dis",
    )

    # initial conditions
    ic = flopy.mf6.ModflowGwfic(gwf, strt=strt, filename=f"{gwfname}.ic")

    # node property flow
    tvk_filename = f"{gwfname}.npf.tvk"
    npf = flopy.mf6.ModflowGwfnpf(
        gwf,
        save_specific_discharge=True,
        icelltype=laytyp,
        k=hk,
        k22=hk,
    )

    # tvk
    # k33 not originally specified in NPF; however, specifying
    # it in tvk in this test should not change the solution to the
    # problem
    tvkspd = {}
    kper = 1
    k33 = 1000.0
    spd = []
    for k in range(nlay):
        for i in range(nrow):
            for j in range(ncol):
                spd.append([(k, i, j), "K33", k33])
    tvkspd[kper] = spd

    tvk = flopy.mf6.ModflowUtltvk(
        npf, print_input=True, perioddata=tvkspd, filename=tvk_filename
    )

    # chd files
    chdspd = []
    for i in range(nrow):
        chdspd.append([(0, i, 0), top + 1])

    chd = flopy.mf6.ModflowGwfchd(
        gwf,
        stress_period_data=chdspd,
        save_flows=False,
        print_flows=True,
        pname="CHD-1",
    )

    # ghb files
    ghbspd = []
    ghbcond = hk * delz * delc / (0.5 * delr)
    for i in range(nrow):
        ghbspd.append([(0, i, ncol - 1), top, ghbcond])

    ghb = flopy.mf6.ModflowGwfghb(
        gwf,
        stress_period_data=ghbspd,
        save_flows=False,
        print_flows=True,
        pname="GHB-1",
    )

    # output control
    oc = flopy.mf6.ModflowGwfoc(
        gwf,
        budget_filerecord=f"{gwfname}.cbc",
        head_filerecord=f"{gwfname}.hds",
        headprintrecord=[("COLUMNS", 10, "WIDTH", 15, "DIGITS", 6, "GENERAL")],
        saverecord=[("HEAD", "LAST"), ("BUDGET", "LAST")],
        printrecord=[("HEAD", "LAST"), ("BUDGET", "LAST")],
    )

    return sim, None


def eval_model(sim):
    print("evaluating model...")

    # budget
    try:
        fname = f"gwf_{sim.name}.lst"
        ws = sim.simpath
        fname = os.path.join(ws, fname)
        lst = flopy.utils.Mf6ListBudget(
            fname, budgetkey="VOLUME BUDGET FOR ENTIRE MODEL"
        )
        lstra = lst.get_incremental()
    except:
        assert False, f'could not load data from "{fname}"'

    # This is the answer to this problem.
    sp_x = []
    for kper, bud in enumerate(lstra):
        sp_x.append(bud)

    # comment when done testing
    print(f"Total outflow in stress period 1 is {str(sp_x[0][8])}")
    print(
        f"Total outflow in stress period 2 after increasing K33 should have no effect on final solution"
    )
    errmsg = f"Period 2 budget should be exactly the same as period 1"
    assert sp_x[0][8] == sp_x[1][8], errmsg


@pytest.mark.parametrize(
    "name",
    ex,
)
def test_mf6model(name, function_tmpdir, targets):
    ws = str(function_tmpdir)
    test = TestFramework()
    test.build(build_model, 0, ws)
    test.run(
        TestSimulation(
            name=name, exe_dict=targets, exfunc=eval_model, idxsim=0
        ),
        ws,
    )
