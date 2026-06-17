import os
import sys
import imas
import numpy
import random

from fusionpy.iofiles.Namelist    import Namelist
from fusionpy.iofiles.plasmastate import get_instate_vars

type_none = type(None)

def get_imas_vars():

    imas_data['species']     = {}
    imas_data['sources']     = {}
    imas_data['equilibrium'] = {}

    imas_data['equilibrium']['time'] = {}
    imas_data['equilibrium']['time']['data'] = {}
    imas_data['equilibrium']['time']['unit'] = {}
    imas_data['equilibrium']['time']['info'] = {}

    return imas_data


def read_imas_data(fpath):
    imas_db = imas.DBEntry("imas:hdf5?path=%s" % fpath,"r")

    ntms           = imas_db.get("ntms",            autoconvert=False)
    summary        = imas_db.get("summary",         autoconvert=False)
    equilibrium    = imas_db.get("equilibrium",     autoconvert=False)
    core_sources   = imas_db.get("core_sources",    autoconvert=False)
    core_profiles  = imas_db.get("core_profiles",   autoconvert=False)
    core_transport = imas_db.get("core_transport",  autoconvert=False)

   #print(dir(summary.global_quantities.tau_energy.source))
 
   #print(summary.global_quantities.energy_mhd.value)
   #print(dir(core_profiles.global_quantities))
   #print(dir(summary.global_quantities))
   #print(summary.plasma_duration.value)
   #print(dir(equilibrium))
   #print(core_transport.time)
   #for i in range(len(core_transport.model)):
   #    print(dir(core_transport.model[i].profiles_1d[0]))
   #print(dir(summary.global_quantities.fusion_gain.source))
   #print(summary.global_quantities.greenwald_fraction.value)
   #print(dir(equilibrium.time_slice[0].global_quantities))
   #return 0
   #sys.exit()

    tau_energy = abs(summary.global_quantities.tau_energy.value.value[0])

    nb_power   = abs(summary.heating_current_drive.nbi[0].power.value.value[0])
    nb_current = abs(summary.heating_current_drive.nbi[0].current.value.value[0])
    ec_power   = abs(summary.heating_current_drive.ec[0].power.value.value[0])
    ec_current = abs(summary.heating_current_drive.ec[0].current.value.value[0])
    lh_power   = abs(summary.heating_current_drive.lh[0].power.value.value[0])
    lh_current = abs(summary.heating_current_drive.lh[0].current.value.value[0])


    time_id = 0
    prof_id = 0

# EQUILIBRIUM
    eq = {}

    eq['time']                   = equilibrium.time.value[0]

    eq['r0']                     = equilibrium.vacuum_toroidal_field.r0.value
    eq['b0']                     = equilibrium.vacuum_toroidal_field.b0.value[0]

    eq['rbdry']                  = equilibrium.time_slice[time_id].boundary.outline.r.value
    eq['zbdry']                  = equilibrium.time_slice[time_id].boundary.outline.z.value

    # 1-D PROFILES
    eq['q']                      = equilibrium.time_slice[time_id].profiles_1d.q.value
    eq['psi']                    = equilibrium.time_slice[time_id].profiles_1d.psi.value
    eq['phi']                    = equilibrium.time_slice[time_id].profiles_1d.phi.value
    eq['fpol']                   = equilibrium.time_slice[time_id].profiles_1d.f.value
    eq['psipol']                 = equilibrium.time_slice[time_id].profiles_1d.psi.value
    eq['pprime']                 = equilibrium.time_slice[time_id].profiles_1d.dpressure_dpsi.value
    eq['ffprime']                = equilibrium.time_slice[time_id].profiles_1d.f_df_dpsi.value
    eq['jphi_1d']                = equilibrium.time_slice[time_id].profiles_1d.j_phi.value
    eq['jtor_1d']                = equilibrium.time_slice[time_id].profiles_1d.j_tor.value
    eq['jpar_1d']                = equilibrium.time_slice[time_id].profiles_1d.j_parallel.value
    eq['rho_tor']                = equilibrium.time_slice[time_id].profiles_1d.rho_tor.value
    eq['beta_pol']               = equilibrium.time_slice[time_id].profiles_1d.beta_pol.value
    eq['psi_norm']               = equilibrium.time_slice[time_id].profiles_1d.psi_norm.value
    eq['pressure']               = equilibrium.time_slice[time_id].profiles_1d.pressure.value
    eq['r_inboard']              = equilibrium.time_slice[time_id].profiles_1d.r_inboard.value
    eq['r_outboard']             = equilibrium.time_slice[time_id].profiles_1d.r_outboard.value
    eq['mass_density']           = equilibrium.time_slice[time_id].profiles_1d.mass_density.value
    eq['rho_tor_norm']           = equilibrium.time_slice[time_id].profiles_1d.rho_tor_norm.value
    eq['magnetic_shear']         = equilibrium.time_slice[time_id].profiles_1d.magnetic_shear.value

    eq['gm1']                    = equilibrium.time_slice[time_id].profiles_1d.gm1.value
    eq['gm2']                    = equilibrium.time_slice[time_id].profiles_1d.gm2.value
    eq['gm3']                    = equilibrium.time_slice[time_id].profiles_1d.gm3.value
    eq['gm4']                    = equilibrium.time_slice[time_id].profiles_1d.gm4.value
    eq['gm5']                    = equilibrium.time_slice[time_id].profiles_1d.gm5.value
    eq['gm6']                    = equilibrium.time_slice[time_id].profiles_1d.gm6.value
    eq['gm7']                    = equilibrium.time_slice[time_id].profiles_1d.gm7.value
    eq['gm8']                    = equilibrium.time_slice[time_id].profiles_1d.gm8.value
    eq['gm9']                    = equilibrium.time_slice[time_id].profiles_1d.gm9.value

    eq['area']                   = equilibrium.time_slice[time_id].profiles_1d.area.value
    eq['volume']                 = equilibrium.time_slice[time_id].profiles_1d.volume.value
    eq['surface']                = equilibrium.time_slice[time_id].profiles_1d.surface.value
    eq['elongation']             = equilibrium.time_slice[time_id].profiles_1d.elongation.value
    eq['trapped_fraction']       = equilibrium.time_slice[time_id].profiles_1d.trapped_fraction.value
    eq['triangularity_upper']    = equilibrium.time_slice[time_id].profiles_1d.triangularity_upper.value
    eq['triangularity_lower']    = equilibrium.time_slice[time_id].profiles_1d.triangularity_lower.value
    eq['squareness_upper_outer'] = equilibrium.time_slice[time_id].profiles_1d.squareness_upper_outer.value
    eq['squareness_upper_inner'] = equilibrium.time_slice[time_id].profiles_1d.squareness_upper_inner.value
    eq['squareness_lower_outer'] = equilibrium.time_slice[time_id].profiles_1d.squareness_lower_outer.value
    eq['squareness_lower_inner'] = equilibrium.time_slice[time_id].profiles_1d.squareness_lower_inner.value

    eq['darea_dpsi']             = equilibrium.time_slice[time_id].profiles_1d.darea_dpsi.value
    eq['dvolume_dpsi']           = equilibrium.time_slice[time_id].profiles_1d.dvolume_dpsi.value
    eq['dpsi_drho_tor']          = equilibrium.time_slice[time_id].profiles_1d.dpsi_drho_tor.value
    eq['darea_drho_tor']         = equilibrium.time_slice[time_id].profiles_1d.darea_drho_tor.value
    eq['dvolume_drho_tor']       = equilibrium.time_slice[time_id].profiles_1d.dvolume_drho_tor.value

    eq['b_min']                  = equilibrium.time_slice[time_id].profiles_1d.b_min.value
    eq['b_max']                  = equilibrium.time_slice[time_id].profiles_1d.b_max.value
    eq['b_average']              = equilibrium.time_slice[time_id].profiles_1d.b_average.value
    eq['b_field_min']            = equilibrium.time_slice[time_id].profiles_1d.b_field_min.value
    eq['b_field_max']            = equilibrium.time_slice[time_id].profiles_1d.b_field_max.value
    eq['b_field_average']        = equilibrium.time_slice[time_id].profiles_1d.b_field_average.value

    # 2-D PROFILES
    eq['rgrid']                  = equilibrium.time_slice[time_id].profiles_2d[prof_id].grid.dim1.value
    eq['zgrid']                  = equilibrium.time_slice[time_id].profiles_2d[prof_id].grid.dim2.value
    eq['psirz']                  = equilibrium.time_slice[time_id].profiles_2d[prof_id].psi.value
    eq['bz_2d']                  = equilibrium.time_slice[time_id].profiles_2d[prof_id].b_z.value
    eq['br_2d']                  = equilibrium.time_slice[time_id].profiles_2d[prof_id].b_r.value
    eq['btor_2d']                = equilibrium.time_slice[time_id].profiles_2d[prof_id].b_tor.value
    eq['jphi_2d']                = equilibrium.time_slice[time_id].profiles_2d[prof_id].j_phi.value
    eq['jtor_2d']                = equilibrium.time_slice[time_id].profiles_2d[prof_id].j_tor.value
    eq['jpar_2d']                = equilibrium.time_slice[time_id].profiles_2d[prof_id].j_parallel.value

    # 0-D GLOBAL QUNATITIES
    eq['ip']                     = equilibrium.time_slice[time_id].global_quantities.ip.value
    eq['li_3']                   = equilibrium.time_slice[time_id].global_quantities.li_3.value
    eq['q_95']                   = equilibrium.time_slice[time_id].global_quantities.q_95.value
    eq['w_mhd']                  = equilibrium.time_slice[time_id].global_quantities.w_mhd.value
    eq['q_min']                  = equilibrium.time_slice[time_id].global_quantities.q_min.value
    eq['q_axis']                 = equilibrium.time_slice[time_id].global_quantities.q_axis.value
    eq['area_sep']               = equilibrium.time_slice[time_id].global_quantities.area.value
    eq['psi_axis']               = equilibrium.time_slice[time_id].global_quantities.psi_axis.value
    eq['psi_bdry']               = equilibrium.time_slice[time_id].global_quantities.psi_boundary.value
    eq['volume_sep']             = equilibrium.time_slice[time_id].global_quantities.volume.value
    eq['v_external']             = equilibrium.time_slice[time_id].global_quantities.v_external.value
    eq['energy_mhd']             = equilibrium.time_slice[time_id].global_quantities.energy_mhd.value
    eq['mag_axis_r']             = equilibrium.time_slice[time_id].global_quantities.magnetic_axis.r.value
    eq['mag_axis_z']             = equilibrium.time_slice[time_id].global_quantities.magnetic_axis.z.value
    eq['surface_spe']            = equilibrium.time_slice[time_id].global_quantities.surface.value
    eq['beta_normal']            = equilibrium.time_slice[time_id].global_quantities.beta_normal.value
    eq['beta_pol_sep']           = equilibrium.time_slice[time_id].global_quantities.beta_pol.value
    eq['beta_tor_sep']           = equilibrium.time_slice[time_id].global_quantities.beta_tor.value
    eq['mag_axis_btor']          = equilibrium.time_slice[time_id].global_quantities.magnetic_axis.b_tor.value
    eq['current_centre_r']       = equilibrium.time_slice[time_id].global_quantities.current_centre.r.value
    eq['current_centre_z']       = equilibrium.time_slice[time_id].global_quantities.current_centre.z.value
    eq['rho_tor_boundary']       = equilibrium.time_slice[time_id].global_quantities.rho_tor_boundary.value
    eq['plasma_inductance']      = equilibrium.time_slice[time_id].global_quantities.plasma_inductance.value
    eq['plasma_resistance']      = equilibrium.time_slice[time_id].global_quantities.plasma_resistance.value

# DENSITY AND TEMPERATURE PROFILES ELECTRONS, IONS, AND FAST IONS

    species                  = {}

    species['time']          = core_profiles.time.value

    species['rho']           = core_profiles.profiles_1d[prof_id].grid.rho_tor_norm.value
    species['p_th']          = core_profiles.profiles_1d[prof_id].pressure_thermal.value         # pi_tot + pe
    species['volume']        = core_profiles.profiles_1d[prof_id].grid.volume.value
    species['pbeam_par']     = core_profiles.profiles_1d[prof_id].pressure_parallel.value
    species['pbeam_per']     = core_profiles.profiles_1d[prof_id].pressure_perpendicular.value

    species['ne']            = core_profiles.profiles_1d[prof_id].electrons.density.value
    species['te']            = core_profiles.profiles_1d[prof_id].electrons.temperature.value
    species['pe']            = core_profiles.profiles_1d[prof_id].electrons.pressure.value
    species['pthe']          = core_profiles.profiles_1d[prof_id].electrons.pressure_thermal.value

    species['zeff']          = core_profiles.profiles_1d[prof_id].zeff.value
    species['ti_avg']        = core_profiles.profiles_1d[prof_id].t_i_average.value
    species['pi_tot']        = core_profiles.profiles_1d[prof_id].pressure_ion_total.value

    species['nspecs']        = len(core_profiles.profiles_1d[prof_id].ion) 
    species['spec_name']     = [None for i in range(species['nspecs'])]

    species['N_imp_ions']    = 0
    species['N_nbi_ions']    = 0
    species['N_thi_ions']    = 0
    species['N_fus_ions']    = 0

    species['F_imp_ions']    = []
    species['F_nbi_ions']    = []
    species['F_thi_ions']    = []
    species['F_fus_ions']    = []

    species['A_imp_ions']    = []
    species['A_nbi_ions']    = []
    species['A_thi_ions']    = []
    species['A_fus_ions']    = []

    species['Z_imp_ions']    = []
    species['Z_nbi_ions']    = []
    species['Z_thi_ions']    = []
    species['Z_fus_ions']    = []

    species['name_imp_ions'] = []
    species['name_nbi_ions'] = []
    species['name_thi_ions'] = []
    species['name_fus_ions'] = []

    Zeff = numpy.zeros(numpy.size(species['rho']))

    species['ions'] = {}
    for ispec in range(species['nspecs']):
        spec_name = str(core_profiles.profiles_1d[0].ion[ispec].label)
        species['spec_name'][ispec] = spec_name

        species['ions'][spec_name]          = {}
        species['ions'][spec_name]['A']     = float(core_profiles.profiles_1d[prof_id].ion[ispec].element[0].a)
        species['ions'][spec_name]['Z']     = float(core_profiles.profiles_1d[prof_id].ion[ispec].element[0].z_n)
        species['ions'][spec_name]['ni']    = core_profiles.profiles_1d[prof_id].ion[ispec].density.value
        species['ions'][spec_name]['ti']    = core_profiles.profiles_1d[prof_id].ion[ispec].temperature.value
        species['ions'][spec_name]['nf']    = core_profiles.profiles_1d[prof_id].ion[ispec].density_fast.value
        species['ions'][spec_name]['nthi']  = core_profiles.profiles_1d[prof_id].ion[ispec].density_thermal.value
        species['ions'][spec_name]['pthi']  = core_profiles.profiles_1d[prof_id].ion[ispec].pressure_thermal.value
        species['ions'][spec_name]['vrad']  = core_profiles.profiles_1d[prof_id].ion[ispec].velocity.radial.value
        species['ions'][spec_name]['vdia']  = core_profiles.profiles_1d[prof_id].ion[ispec].velocity.diamagnetic.value
        species['ions'][spec_name]['vpar']  = core_profiles.profiles_1d[prof_id].ion[ispec].velocity.parallel.value
        species['ions'][spec_name]['vpol']  = core_profiles.profiles_1d[prof_id].ion[ispec].velocity.poloidal.value
        species['ions'][spec_name]['vtor']  = core_profiles.profiles_1d[prof_id].ion[ispec].velocity.toroidal.value
        species['ions'][spec_name]['omega'] = core_profiles.profiles_1d[prof_id].ion[ispec].rotation_frequency_tor.value
        species['ions'][spec_name]['pfpar'] = core_profiles.profiles_1d[prof_id].ion[ispec].pressure_fast_parallel.value
        species['ions'][spec_name]['pfper'] = core_profiles.profiles_1d[prof_id].ion[ispec].pressure_fast_perpendicular.value

       #species['ions'][spec_name]['vpol'] = core_profiles.profiles_1d[prof_id].ion[ispec].velocity_pol.value
       #species['ions'][spec_name]['vtor'] = core_profiles.profiles_1d[prof_id].ion[ispec].velocity_tor.value

        Zeff += species['ions'][spec_name]['ni'] * species['ions'][spec_name]['Z']**2 / species['ne']
#   species['zeff'] = Zeff


# AUXILIARY HEATING AND LOSSES
    sources = {}
    sources['time'] = core_sources.time.value
    nsrcs = len(core_sources.source)

    nbi_src_flag = False

    for isrc in range(nsrcs):
        src_name = core_sources.source[isrc].identifier.name.value
        if   src_name == 'nbi':
             nbi_src_flag = True
             sources[src_name] = {}
             sources[src_name]['A']         = float(core_sources.source[isrc].profiles_1d[prof_id].ion[ispec].element[0].a)
             sources[src_name]['Z']         = float(core_sources.source[isrc].profiles_1d[prof_id].ion[ispec].element[0].z_n)
             sources[src_name]['info']      = core_sources.source[isrc].identifier.description.value
             sources[src_name]['rho']       = core_sources.source[isrc].profiles_1d[prof_id].grid.rho_tor_norm.value
             sources[src_name]['jp_nb']     = core_sources.source[isrc].profiles_1d[prof_id].j_parallel.value
             sources[src_name]['pe_nb']     = core_sources.source[isrc].profiles_1d[prof_id].electrons.energy.value
             sources[src_name]['pi_nb']     = core_sources.source[isrc].profiles_1d[prof_id].total_ion_energy.value
             sources[src_name]['se_nb']     = core_sources.source[isrc].profiles_1d[prof_id].electrons.particles.value
             sources[src_name]['si_nb']     = [0.0 for item in sources[src_name]['rho']]
             for i in range(species['nspecs']):
                 if any(core_sources.source[isrc].profiles_1d[prof_id].ion[i].particles.value):
                    sources[src_name]['si_nb']  = [i+j for (i,j) in zip(sources[src_name]['si_nb'],core_sources.source[isrc].profiles_1d[prof_id].ion[i].particles.value)]
        elif src_name == 'ec':
             sources[src_name] = {}
             sources[src_name]['info']      = core_sources.source[isrc].identifier.description.value
             sources[src_name]['rho']       = core_sources.source[isrc].profiles_1d[prof_id].grid.rho_tor_norm.value
             sources[src_name]['jp_ec']     = core_sources.source[isrc].profiles_1d[prof_id].j_parallel.value
             sources[src_name]['pe_ec']     = core_sources.source[isrc].profiles_1d[prof_id].electrons.energy.value
            #print(src_name)
            #print(sources[src_name]['pe_ec'])
        elif src_name == 'ic':
             sources[src_name] = {}
             sources[src_name]['info']      = core_sources.source[isrc].identifier.description.value
             sources[src_name]['rho']       = core_sources.source[isrc].profiles_1d[prof_id].grid.rho_tor_norm.value
             sources[src_name]['jp_ic']     = core_sources.source[isrc].profiles_1d[prof_id].j_parallel.value
             sources[src_name]['pi_ic']     = core_sources.source[isrc].profiles_1d[prof_id].total_ion_energy.value
            #print(src_name)
            #print(sources[src_name]['pi_ic'])
        elif src_name == 'lh':
             sources[src_name] = {}
             sources[src_name]['info']      = core_sources.source[isrc].identifier.description.value
             sources[src_name]['rho']       = core_sources.source[isrc].profiles_1d[prof_id].grid.rho_tor_norm.value
             sources[src_name]['jp_lh']     = core_sources.source[isrc].profiles_1d[prof_id].j_parallel.value
             sources[src_name]['pi_lh']     = core_sources.source[isrc].profiles_1d[prof_id].total_ion_energy.value
             sources[src_name]['pe_lh']     = core_sources.source[isrc].profiles_1d[prof_id].electrons.energy.value
             sources[src_name]['se_lh']     = core_sources.source[isrc].profiles_1d[prof_id].electrons.particles.value
             sources[src_name]['si_lh']     = [0.0 for item in sources[src_name]['rho']]
             for i in range(species['nspecs']):
                 if any(core_sources.source[isrc].profiles_1d[prof_id].ion[i].particles.value):
                    sources[src_name]['si_lh']  = [i+j for (i,j) in zip(sources[src_name]['si_lh'],core_sources.source[isrc].profiles_1d[prof_id].ion[i].particles.value)]
        elif src_name == 'ohmic':
             sources[src_name] = {}
             sources[src_name]['info']      = core_sources.source[isrc].identifier.description.value
             sources[src_name]['rho']       = core_sources.source[isrc].profiles_1d[prof_id].grid.rho_tor_norm.value
             sources[src_name]['jp_ohm']    = core_sources.source[isrc].profiles_1d[prof_id].j_parallel.value
             sources[src_name]['pi_ohm']    = core_sources.source[isrc].profiles_1d[prof_id].total_ion_energy.value
             sources[src_name]['pe_ohm']    = core_sources.source[isrc].profiles_1d[prof_id].electrons.energy.value
             sources[src_name]['se_ohm']    = core_sources.source[isrc].profiles_1d[prof_id].electrons.particles.value
             sources[src_name]['si_ohm']    = [0.0 for item in sources[src_name]['rho']]
             for i in range(species['nspecs']):
                 if any(core_sources.source[isrc].profiles_1d[prof_id].ion[i].particles.value):
                    sources[src_name]['si_ohm']  = [i+j for (i,j) in zip(sources[src_name]['si_ohm'],core_sources.source[isrc].profiles_1d[prof_id].ion[i].particles.value)]
        elif src_name == 'charge_exchange':
             sources[src_name] = {}
             sources[src_name]['info']      = core_sources.source[isrc].identifier.description.value
             sources[src_name]['rho']       = core_sources.source[isrc].profiles_1d[prof_id].grid.rho_tor_norm.value
             sources[src_name]['pi_cx']     = core_sources.source[isrc].profiles_1d[prof_id].total_ion_energy.value
             sources[src_name]['pe_cx']     = core_sources.source[isrc].profiles_1d[prof_id].electrons.energy.value
             sources[src_name]['se_cx']     = core_sources.source[isrc].profiles_1d[prof_id].electrons.particles.value
             sources[src_name]['si_cx']     = [0.0 for item in sources[src_name]['rho']]
             for i in range(species['nspecs']):
                 if any(core_sources.source[isrc].profiles_1d[prof_id].ion[i].particles.value):
                    sources[src_name]['si_cx']  = [i+j for (i,j) in zip(sources[src_name]['si_cx'],core_sources.source[isrc].profiles_1d[prof_id].ion[i].particles.value)]
        elif src_name == 'radiation':
             sources[src_name] = {}
             sources[src_name]['info']      = core_sources.source[isrc].identifier.description.value
             sources[src_name]['rho']       = core_sources.source[isrc].profiles_1d[prof_id].grid.rho_tor_norm.value
             sources[src_name]['pe_rad']    = core_sources.source[isrc].profiles_1d[prof_id].electrons.energy.value
             sources[src_name]['pi_rad']    = core_sources.source[isrc].profiles_1d[prof_id].total_ion_energy.value
             sources[src_name]['se_rad']    = core_sources.source[isrc].profiles_1d[prof_id].electrons.particles.value
             sources[src_name]['si_rad']    = [0.0 for item in sources[src_name]['rho']]
             for i in range(species['nspecs']):
                 if any(core_sources.source[isrc].profiles_1d[prof_id].ion[i].particles.value):
                    sources[src_name]['si_rad']  = [i+j for (i,j) in zip(sources[src_name]['si_rad'],core_sources.source[isrc].profiles_1d[prof_id].ion[i].particles.value)]
        elif src_name == "bootstrap_current":
             sources[src_name] = {}
             sources[src_name]['info']      = core_sources.source[isrc].identifier.description.value
             sources[src_name]['rho']       = core_sources.source[isrc].profiles_1d[prof_id].grid.rho_tor_norm.value
             sources[src_name]['jp_bs']     = core_sources.source[isrc].profiles_1d[prof_id].j_parallel.value
        elif src_name == "synchrotron_radiation":
             sources[src_name] = {}
             sources[src_name]['info']      = core_sources.source[isrc].identifier.description.value
             sources[src_name]['rho']       = core_sources.source[isrc].profiles_1d[prof_id].grid.rho_tor_norm.value
             sources[src_name]['pe_sync']   = core_sources.source[isrc].profiles_1d[prof_id].electrons.energy.value
             sources[src_name]['pi_sync']   = core_sources.source[isrc].profiles_1d[prof_id].total_ion_energy.value
        elif src_name == "cold_neutrals":
             sources[src_name] = {}
             sources[src_name]['info']      = core_sources.source[isrc].identifier.description.value
             sources[src_name]['rho']       = core_sources.source[isrc].profiles_1d[prof_id].grid.rho_tor_norm.value
             sources[src_name]['pe_neut']   = core_sources.source[isrc].profiles_1d[prof_id].electrons.energy.value
             sources[src_name]['pi_neut']   = core_sources.source[isrc].profiles_1d[prof_id].total_ion_energy.value
             sources[src_name]['se_neut']   = core_sources.source[isrc].profiles_1d[prof_id].electrons.particles.value
             sources[src_name]['si_neut']    = [0.0 for item in sources[src_name]['rho']]
             for i in range(species['nspecs']):
                 if any(core_sources.source[isrc].profiles_1d[prof_id].ion[i].particles.value):
                    sources[src_name]['si_neut']  = [i+j for (i,j) in zip(sources[src_name]['si_neut'],core_sources.source[isrc].profiles_1d[prof_id].ion[i].particles.value)]
        elif src_name == "collisional_equipartition":
             sources[src_name] = {}
             sources[src_name]['info']      = core_sources.source[isrc].identifier.description.value
             sources[src_name]['rho']       = core_sources.source[isrc].profiles_1d[prof_id].grid.rho_tor_norm.value
             sources[src_name]['pe_coll']   = core_sources.source[isrc].profiles_1d[prof_id].electrons.energy.value
             sources[src_name]['pi_coll']   = core_sources.source[isrc].profiles_1d[prof_id].total_ion_energy.value
             sources[src_name]['se_coll']   = core_sources.source[isrc].profiles_1d[prof_id].electrons.particles.value
             sources[src_name]['si_coll']  = [0.0 for item in sources[src_name]['rho']]
             for i in range(species['nspecs']):
                 if any(core_sources.source[isrc].profiles_1d[prof_id].ion[i].particles.value):
                    sources[src_name]['si_coll']  = [i+j for (i,j) in zip(sources[src_name]['si_coll'],core_sources.source[isrc].profiles_1d[prof_id].ion[i].particles.value)]
            #print(src_name)
            #print(sources[src_name]['pe_coll'])
            #print(sources[src_name]['pi_coll'])
            #print(sources[src_name]['se_coll'])
            #print(sources[src_name]['si_coll'])
        elif src_name == "pellet":
             sources[src_name] = {}
             sources[src_name]['info']      = core_sources.source[isrc].identifier.description.value
             sources[src_name]['rho']       = core_sources.source[isrc].profiles_1d[prof_id].grid.rho_tor_norm.value
             sources[src_name]['pe_pellet'] = core_sources.source[isrc].profiles_1d[prof_id].electrons.energy.value
             sources[src_name]['pi_pellet'] = core_sources.source[isrc].profiles_1d[prof_id].total_ion_energy.value
             sources[src_name]['se_pellet'] = core_sources.source[isrc].profiles_1d[prof_id].electrons.particles.value
             sources[src_name]['si_pellet'] = [0.0 for item in sources[src_name]['rho']]
             for i in range(species['nspecs']):
                 if any(core_sources.source[isrc].profiles_1d[prof_id].ion[i].particles.value):
                    sources[src_name]['si_pellet']  = [i+j for (i,j) in zip(sources[src_name]['si_pellet'],core_sources.source[isrc].profiles_1d[prof_id].ion[i].particles.value)]
            #print(src_name)
            #print(sources[src_name]['pe_pellet'])
            #print(sources[src_name]['pi_pellet'])
            #print(sources[src_name]['se_pellet'])
            #print(sources[src_name]['si_pellet'])
        elif src_name == "auxiliary":
             sources[src_name] = {}
             sources[src_name]['info']      = core_sources.source[isrc].identifier.description.value
             sources[src_name]['rho']       = core_sources.source[isrc].profiles_1d[prof_id].grid.rho_tor_norm.value
             sources[src_name]['pe_auxi']   = core_sources.source[isrc].profiles_1d[prof_id].electrons.energy.value
             sources[src_name]['pi_auxi']   = core_sources.source[isrc].profiles_1d[prof_id].total_ion_energy.value
             sources[src_name]['se_auxi']   = core_sources.source[isrc].profiles_1d[prof_id].electrons.particles.value
             sources[src_name]['si_auxi']  = [0.0 for item in sources[src_name]['rho']]
             for i in range(species['nspecs']):
                 if any(core_sources.source[isrc].profiles_1d[prof_id].ion[i].particles.value):
                    sources[src_name]['si_auxi']  = [i+j for (i,j) in zip(sources[src_name]['si_auxi'],core_sources.source[isrc].profiles_1d[prof_id].ion[i].particles.value)]
            #print(src_name)
            #print(sources[src_name]['pe_auxi'])
            #print(sources[src_name]['pi_auxi'])
            #print(sources[src_name]['se_auxi'])
            #print(sources[src_name]['si_auxi'])
        elif src_name == "fusion":
             sources[src_name] = {}
             sources[src_name]['info']      = core_sources.source[isrc].identifier.description.value
             sources[src_name]['rho']       = core_sources.source[isrc].profiles_1d[prof_id].grid.rho_tor_norm.value
             sources[src_name]['jp_fus']    = core_sources.source[isrc].profiles_1d[prof_id].j_parallel.value
             sources[src_name]['pe_fus']    = core_sources.source[isrc].profiles_1d[prof_id].electrons.energy.value
             sources[src_name]['pi_fus']    = core_sources.source[isrc].profiles_1d[prof_id].total_ion_energy.value
             sources[src_name]['se_fus']    = core_sources.source[isrc].profiles_1d[prof_id].electrons.particles.value
             sources[src_name]['si_fus']    = [0.0 for item in sources[src_name]['rho']]
             for i in range(species['nspecs']):
                 if any(core_sources.source[isrc].profiles_1d[prof_id].ion[i].particles.value):
                    sources[src_name]['si_fus']  = [round(float(i+j),7) for (i,j) in zip(sources[src_name]['si_fus'],core_sources.source[isrc].profiles_1d[prof_id].ion[i].particles.value)]
            #print(src_name)
            #print(sources[src_name]['pe_fus'])
            #print(sources[src_name]['pi_fus'])
            #print(sources[src_name]['se_fus'])
            #print(sources[src_name]['si_fus'])

# FOCUS
    n_nbi_tot_1d  = numpy.zeros(numpy.size(species['rho']))
    n_thi_tot_1d  = numpy.zeros(numpy.size(species['rho']))
    n_imp_tot_1d  = numpy.zeros(numpy.size(species['rho']))
    n_fus_tot_1d  = numpy.zeros(numpy.size(species['rho']))

    for ispec in range(species['nspecs']):
        spec_name = species['spec_name'][ispec]
        if spec_name in ['T']:
           if any(species['ions'][spec_name]['nf']):
              n_nbi_tot_1d += numpy.array([float(item) for item in species['ions'][spec_name]['nf']])
           if any(species['ions'][spec_name]['nthi']):
              n_thi_tot_1d += numpy.array([float(item) for item in species['ions'][spec_name]['nthi']])
        elif spec_name in ['D']:
           if any(species['ions'][spec_name]['nf']):
              n_nbi_tot_1d += numpy.array([float(item) for item in species['ions'][spec_name]['nf']])
           if any(species['ions'][spec_name]['nthi']):
              n_thi_tot_1d += numpy.array([float(item) for item in species['ions'][spec_name]['nthi']])
        elif spec_name in ['He']:
           if any(species['ions'][spec_name]['nf']):
              n_fus_tot_1d += numpy.array([float(item) for item in species['ions'][spec_name]['nf']])
           if any(species['ions'][spec_name]['nthi']):
              n_imp_tot_1d += numpy.array([float(item) for item in species['ions'][spec_name]['nthi']])
        elif spec_name in ['Ne']:
           if any(species['ions'][spec_name]['nthi']):
              n_imp_tot_1d += numpy.array([float(item) for item in species['ions'][spec_name]['nthi']])
        elif spec_name in ['C']:
           if any(species['ions'][spec_name]['nthi']):
              n_imp_tot_1d += numpy.array([float(item) for item in species['ions'][spec_name]['nthi']])
        elif spec_name in ['B']:
           if any(species['ions'][spec_name]['nthi']):
              n_imp_tot_1d += numpy.array([float(item) for item in species['ions'][spec_name]['nthi']])
        elif spec_name in ['Be']:
           if any(species['ions'][spec_name]['nthi']):
              n_imp_tot_1d += numpy.array([float(item) for item in species['ions'][spec_name]['nthi']])
        elif spec_name in ['W']:
           if any(species['ions'][spec_name]['nthi']):
              n_imp_tot_1d += numpy.array([float(item) for item in species['ions'][spec_name]['nthi']])

   #for ispec in range(species['nspecs']):
   #    spec_name = species['spec_name'][ispec]
   #    if   spec_name in ['T']:
   #         n_thi_tot_1d += species['ions'][spec_name]['nthi']
   #         n_nbi_tot_1d += species['ions'][spec_name]['ni'] - species['ions'][spec_name]['nthi']
   #    elif spec_name in ['D']:
   #         n_thi_tot_1d += species['ions'][spec_name]['nthi']
   #         n_nbi_tot_1d += species['ions'][spec_name]['ni'] - species['ions'][spec_name]['nthi']
   #    elif spec_name in ['He']:
   #         n_imp_tot_1d += species['ions'][spec_name]['nthi']
   #         n_fus_tot_1d += species['ions'][spec_name]['ni'] - species['ions'][spec_name]['nthi']
   #    else:
   #         n_imp_tot_1d += species['ions'][spec_name]['nthi']

    species['tot_nthi']    = n_thi_tot_1d
    species['tot_nfus']    = n_fus_tot_1d
    species['tot_nimp']    = n_imp_tot_1d
    species['tot_nnbi']    = n_nbi_tot_1d
   #if all(item == 0.0 for item in n_nbi_tot_1d):
   #   n_nbi_tot_1d = species['ne']-species['tot_nthi']-species['tot_nimp']-species['tot_nfus']
   #   species['tot_nnbi']        = n_nbi_tot_1d
   #   species['ions']['D']['nf'] = n_nbi_tot_1d
   #else:
   #   species['tot_nnbi']        = n_nbi_tot_1d

    for spec_name in species['spec_name']:
        if spec_name in ['T']:
           if any(species['ions'][spec_name]['nf']):
              n_nbi_tot = sum(n_nbi_tot_1d)
              species['name_nbi_ions'].append(spec_name)
              species['N_nbi_ions'] += 1
              species['A_nbi_ions'].append(species['ions'][spec_name]['A'])
              species['Z_nbi_ions'].append(species['ions'][spec_name]['Z'])
              species['F_nbi_ions'].append(round(float(sum(species['ions'][spec_name]['nf']) / n_nbi_tot),2))
           if any(species['ions'][spec_name]['nthi']):
              n_thi_tot = sum(n_thi_tot_1d)
              species['name_thi_ions'].append(spec_name)
              species['N_thi_ions'] += 1
              species['A_thi_ions'].append(species['ions'][spec_name]['A'])
              species['Z_thi_ions'].append(species['ions'][spec_name]['Z'])
              species['F_thi_ions'].append(round(float(sum(species['ions'][spec_name]['nthi']) / n_thi_tot),2))
        elif spec_name in ['D']:
           if any(species['ions'][spec_name]['nf']) or nbi_src_flag:
              n_nbi_tot = sum(n_nbi_tot_1d)
              species['name_nbi_ions'].append(spec_name)
              species['N_nbi_ions'] += 1
              species['A_nbi_ions'].append(species['ions'][spec_name]['A'])
              species['Z_nbi_ions'].append(species['ions'][spec_name]['Z'])
              species['F_nbi_ions'].append(round(float(sum(species['ions'][spec_name]['nf']) / n_nbi_tot),2))
           if any(species['ions'][spec_name]['nthi']):
              n_thi_tot = sum(n_thi_tot_1d)
              species['name_thi_ions'].append(spec_name)
              species['N_thi_ions'] += 1
              species['A_thi_ions'].append(species['ions'][spec_name]['A'])
              species['Z_thi_ions'].append(species['ions'][spec_name]['Z'])
              species['F_thi_ions'].append(round(float(sum(species['ions'][spec_name]['nthi']) / n_thi_tot),2))
        elif spec_name in ['He']:
           if any(species['ions'][spec_name]['nf']):
              n_fus_tot = sum(n_fus_tot_1d)
              species['name_fus_ions'].append(spec_name)
              species['N_fus_ions'] += 1
              species['A_fus_ions'].append(species['ions'][spec_name]['A'])
              species['Z_fus_ions'].append(species['ions'][spec_name]['Z'])
              species['F_fus_ions'].append(round(float(sum(species['ions'][spec_name]['nf']) / n_fus_tot),2))
           if any(species['ions'][spec_name]['nthi']):
              n_imp_tot = sum(n_imp_tot_1d)
              species['name_imp_ions'].append(spec_name)
              species['N_imp_ions'] += 1
              species['A_imp_ions'].append(species['ions'][spec_name]['A'])
              species['Z_imp_ions'].append(species['ions'][spec_name]['Z'])
              species['F_imp_ions'].append(round(float(sum(species['ions'][spec_name]['nthi']) / n_imp_tot),2))
        elif spec_name in ['Ne','C','B','W']:
           if any(species['ions'][spec_name]['nthi']):
              n_imp_tot = sum(n_imp_tot_1d)
              species['name_imp_ions'].append(spec_name)
              species['N_imp_ions'] += 1
              species['A_imp_ions'].append(species['ions'][spec_name]['A'])
              species['Z_imp_ions'].append(species['ions'][spec_name]['Z'])
              species['F_imp_ions'].append(round(float(sum(species['ions'][spec_name]['nthi']) / n_imp_tot),2))

    imas_data = {}
    imas_data['species']     = species
    imas_data['sources']     = sources
    imas_data['equilibrium'] = eq

    return imas_data

def to_instate(fpath,fname="",setParam={}):
    imas_data = read_imas_data(fpath=fpath)

    instate = get_instate_vars()

    if   'SHOT_ID' in setParam:
          SHOT_ID = setParam['SHOT_ID']
    elif 'shot_id' in setParam:
          SHOT_ID = setParam['shot_id']
    else:
          SHOT_ID = "baseline"

    if   'TIME_ID' in setParam:
          TIME_ID = setParam['TIME_ID']
    elif 'time_id' in setParam:
          TIME_ID = setParam['time_id']
    else:
          TIME_ID = "%05d" % int(imas_data['equilibrium']['time']*100)

    if   'TOKAMAK_ID' in setParam:
          TOKAMAK_ID = setParam['TOKAMAK_ID']
    elif 'tokamak_id' in setParam:
          TOKAMAK_ID = setParam['tokamak_id']
    else:
          TOKAMAK_ID = "iter"

    if   'LIMITER_MODEL' in setParam:
          LIMITER_MODEL = setParam['LIMITER_MODEL']
    elif 'limiter_model' in setParam:
          LIMITER_MODEL = setParam['limiter_model']
    else:
          LIMITER_MODEL = 1

    instate['SHOT_ID']       = [SHOT_ID]
    instate['TIME_ID']       = [TIME_ID]
    instate['TOKAMAK_ID']    = [TOKAMAK_ID]
    instate['MODEL_SHAPE']   = [0]
    instate['DENSITY_MODEL'] = [0]

    instate['R0']     = [round(    imas_data['equilibrium']['r0'],           7)]
    instate['B0']     = [round(abs(imas_data['equilibrium']['b0']),          7)]
    instate['IP']     = [round(abs(imas_data['equilibrium']['ip']) * 1.0e-6, 7)]

    imas_data['equilibrium']['elongation_sep'] = numpy.max(imas_data['equilibrium']['elongation'])

    delta_upper = numpy.max(imas_data['equilibrium']['triangularity_upper'])
    delta_lower = numpy.max(imas_data['equilibrium']['triangularity_lower'])
    imas_data['equilibrium']['triangularity_sep'] = (delta_upper + delta_lower) / 2.0

    instate['KAPPA']  = [round(imas_data['equilibrium']['elongation_sep'],       7)]
    instate['DELTA']  = [round(imas_data['equilibrium']['triangularity_sep'],    7)]

    r_max = numpy.max(imas_data['equilibrium']['rgrid'])
    r_min = numpy.min(imas_data['equilibrium']['rgrid'])
    imas_data['equilibrium']['eps'] = round((r_max - r_min)/(r_max + r_min), 2)
    imas_data['equilibrium']['a0']  = round(imas_data['equilibrium']['r0'] * imas_data['equilibrium']['eps'], 2)

    instate['RMAJOR'] = [round(imas_data['equilibrium']['r0'],               7)]
    instate['AMINOR'] = [round(imas_data['equilibrium']['a0'],               7)]
    instate['ASPECT'] = [round(imas_data['equilibrium']['eps'],              7)]

    instate['N_ION']    = [imas_data['species']['N_thi_ions']]
    instate['Z_ION']    =  imas_data['species']['Z_thi_ions']
    instate['A_ION']    =  imas_data['species']['A_thi_ions']
    instate['F_ION']    =  imas_data['species']['F_thi_ions']
    instate['N_IMP']    = [imas_data['species']['N_imp_ions']]
    instate['Z_IMP']    =  imas_data['species']['Z_imp_ions']
    instate['A_IMP']    =  imas_data['species']['A_imp_ions']
    instate['F_IMP']    =  imas_data['species']['F_imp_ions']
    instate['N_MIN']    = [0]
    instate['Z_MIN']    = [0]
    instate['A_MIN']    = [0]
    instate['N_BEAM']   = [imas_data['species']['N_nbi_ions']]
    instate['Z_BEAM']   =  imas_data['species']['Z_nbi_ions'] if len(imas_data['species']['Z_nbi_ions']) != 0 else [0]
    instate['A_BEAM']   =  imas_data['species']['A_nbi_ions'] if len(imas_data['species']['A_nbi_ions']) != 0 else [0]
    instate['N_FUSION'] = [imas_data['species']['N_fus_ions']]
    instate['Z_FUSION'] =  imas_data['species']['Z_fus_ions'] if len(imas_data['species']['Z_fus_ions']) != 0 else [0]
    instate['A_FUSION'] =  imas_data['species']['A_fus_ions'] if len(imas_data['species']['A_fus_ions']) != 0 else [0]

    instate['RHO']    = [round(float(i),2) for i in imas_data['equilibrium']['rho_tor_norm']  ]
    instate['NRHO']   = [numpy.size(instate['RHO'])                                    ]
   #instate['PSIPOL'] = [round(float(i),7) for i in imas_data['equilibrium']['psipol']        ]

    instate['TE']      = [round(float(i)*1.0e-3 ,7) for i in imas_data['species']['te']        ]
    instate['TI']      = [round(float(i)*1.0e-3 ,7) for i in imas_data['species']['ti_avg']    ]
    #nstate['TZ']      = [round(float(i)*1.0e-3 ,7) for i in imas_data['species']['ti_avg']    ]
    instate['NE']      = [round(float(i)*1.0e-19,7) for i in imas_data['species']['ne']        ]
    instate['NI']      = [round(float(i)*1.0e-19,7) for i in imas_data['species']['tot_nthi']]
    #nstate['NZ']      = [round(float(i)*1.0e-19,7) for i in imas_data['species']['tot_nimp']]

    instate['ZEFF']    = [round(float(i),2) for i in imas_data['species']['zeff']             ]
    instate['OMEGA']   = [round(float(i),7) for i in imas_data['species']['ions']['D']['vtor']]

    instate['PSI_AXIS'] = [round(imas_data['equilibrium']['psi_axis'], 7)]
    instate['PSI_BDRY'] = [round(imas_data['equilibrium']['psi_bdry'], 7)]
    instate['RHOPSI']   = [round(i,7) for i in numpy.sqrt(imas_data['equilibrium']['psi_norm'])]

    instate['SCALE_NE']            = [1.0]
    instate['SCALE_NI']            = [1.0]
    instate['SCALE_TE']            = [1.0]
    instate['SCALE_TI']            = [1.0]
    instate['SCALE_SION']          = [1.0]
    instate['SCALE_SE_NB']         = [1.0]
    instate['SCALE_SI_NB']         = [1.0]
    instate['SCALE_SE_PELLET']     = [1.0]
    instate['SCALE_DENSITY_BEAM']  = [1.0]
    instate['SCALE_SE_IONIZATION'] = [1.0]
    instate['SCALE_SI_IONIZATION'] = [1.0]
    instate['SCALE_PE_IONIZATION'] = [1.0]
    instate['SCALE_PI_IONIZATION'] = [1.0]

    q_min_shift = 1.1 - min(imas_data['equilibrium']['q'])
    imas_data['equilibrium']['q'] += q_min_shift

    instate['Q']       = [round(float(i),7) for i in imas_data['equilibrium']['q']]
    instate['P_EQ']    = [round(float(i),7) for i in imas_data['equilibrium']['pressure']]
   #instate['PPRIME']  = [round(float(i),7) for i in imas_data['equilibrium']['pprime']]
   #instate['FFPRIME'] = [round(float(i),7) for i in imas_data['equilibrium']['ffprime']]
    instate['J_TOT']   = [round(float(abs(i)*1.0e-6),7) for i in imas_data['equilibrium']['jpar_1d']]

    if any(imas_data['sources']['ohmic']['jp_ohm' ]):
       instate['J_OH']    = [round(float(abs(i)*1.0e-6),7) for i in (imas_data['sources']['ohmic']['jp_ohm' ])]
    else:
       instate['J_OH'] = [round(0.0,7) for i in range(instate['NRHO'][0])          ]

    if any(imas_data['sources']['nbi']['jp_nb' ]):
       instate['J_NB']    = [round(float(abs(i)*1.0e-6),7) for i in (imas_data['sources']['nbi']['jp_nb'  ])]
    else:
       instate['J_NB'] = [round(0.0,7) for i in range(instate['NRHO'][0])          ]

    if any(imas_data['sources']['bootstrap_current']['jp_bs' ]):
       instate['J_BS']    = [round(float(abs(i)*1.0e-6),7) for i in (imas_data['sources']['bootstrap_current']['jp_bs'  ])]
    else:
       oinstate['J_BS'] = [round(0.0,7) for i in range(instate['NRHO'][0])          ]

    if any(imas_data['sources']['ec']['jp_ec' ]):
       instate['J_EC']    = [round(float(abs(i)*1.0e-6),7) for i in (imas_data['sources']['ec']['jp_ec'  ])]
    else:
       instate['J_EC'] = [round(0.0,7) for i in range(instate['NRHO'][0])          ]

    if any(imas_data['sources']['ic']['jp_ic' ]):
       instate['J_IC']    = [round(float(abs(i)*1.0e-6),7) for i in (imas_data['sources']['ic']['jp_ic'  ])]
    else:
       instate['J_IC'] = [round(0.0,7) for i in range(instate['NRHO'][0])          ]

    if any(imas_data['sources']['lh']['jp_lh' ]):
       instate['J_LH']    = [round(float(abs(i)*1.0e-6),7) for i in (imas_data['sources']['lh']['jp_lh'  ])]
    else:
       instate['J_LH'] = [round(0.0,7) for i in range(instate['NRHO'][0])          ]

    if any(imas_data['sources']['nbi']['pe_nb']):
       instate['PE_NB']   = [round(float(i*1.0e-6),7) for i in (imas_data['sources']['nbi']['pe_nb'])]
    else:
       instate['PE_NB'] = [round(0.0,7) for i in range(instate['NRHO'][0])          ]

    if any(imas_data['sources']['nbi']['pi_nb']):
       instate['PI_NB']   = [round(float(i*1.0e-6),7) for i in (imas_data['sources']['nbi']['pi_nb'])]
    else:
       instate['PI_NB'] = [round(0.0,7) for i in range(instate['NRHO'][0])          ]

    if any(imas_data['sources']['ec']['pe_ec']):
       instate['PE_EC']   = [round(float(i*1.0e-6),7) for i in (imas_data['sources']['ec']['pe_ec'])]
    else:
       instate['PE_EC'] = [round(0.0,7) for i in range(instate['NRHO'][0])          ]

    if any(imas_data['sources']['ic']['pi_ic']):
       instate['PI_IC']   = [round(float(i*1.0e-6),7) for i in (imas_data['sources']['ic']['pi_ic'])]
    else:
       instate['PI_IC'] = [round(0.0,7) for i in range(instate['NRHO'][0])          ]

    if any(imas_data['sources']['lh']['pe_lh']):
       instate['PE_LH']   = [round(float(i*1.0e-6),7) for i in (imas_data['sources']['lh']['pe_lh'])]
    else:
       instate['PE_LH'] = [round(0.0,7) for i in range(instate['NRHO'][0])          ]

    if any(imas_data['sources']['lh']['pi_lh']):
       instate['PI_LH']   = [round(float(i*1.0e-6),7) for i in (imas_data['sources']['lh']['pi_lh'])]
    else:
       instate['PI_LH'] = [round(0.0,7) for i in range(instate['NRHO'][0])          ]

    if any(imas_data['sources']['fusion']['pe_fus']):
       instate['PE_FUS']   = [round(float(i*1.0e-6),7) for i in (imas_data['sources']['fusion']['pe_fus'])]
    else:
       instate['PE_FUS'] = [round(0.0,7) for i in range(instate['NRHO'][0])          ]

    if any(imas_data['sources']['fusion']['pi_fus']):
       instate['PI_FUS']   = [round(float(i*1.0e-6),7) for i in (imas_data['sources']['fusion']['pi_fus'])]
    else:
       instate['PI_FUS'] = [round(0.0,7) for i in range(instate['NRHO'][0])          ]

    instate['P_EI']   = [round(float(i*1.0e-6),7) for i in (imas_data['sources']['collisional_equipartition']['pe_coll'])]
    instate['P_RAD']  = [round(float(i*1.0e-6),7) for i in (imas_data['sources']['radiation']['pe_rad']                 )]
    instate['P_OHM']  = [round(float(i*1.0e-6),7) for i in (imas_data['sources']['ohmic']['pe_ohm']                     )]

    if any(imas_data['sources']['charge_exchange']['pe_cx']):
       instate['PE_CX'] = [round(float(i*1.0e-6),7) for i in (imas_data['sources']['charge_exchange']['pe_cx']         )]
    else:
       instate['PE_CX'] = [round(0.0,7) for i in range(instate['NRHO'][0])          ]

    if any(imas_data['sources']['charge_exchange']['pi_cx']):
       instate['PI_CX'] = [round(float(i*1.0e-6),7) for i in (imas_data['sources']['charge_exchange']['pi_cx']         )]
    else:
       instate['PI_CX'] = [round(0.0,7) for i in range(instate['NRHO'][0])          ]

    if any(imas_data['sources']['nbi']['si_nb']):
       instate['SE_NB'] = [round(float(i*1.0e-19),7) for i in (imas_data['sources']['nbi']['si_nb']                    )]
    else:
       instate['SE_NB'] = [round(0.0,7) for i in range(instate['NRHO'][0])          ]

   #if any(imas_data['sources']['nbi']['si_nb']):
   #   instate['SI_NB'] = [round(float(i*1.0e-19),7) for i in (imas_data['sources']['nbi']['si_nb']                    )]
   #else:
   #   instate['SI_NB'] = [round(0.0,7) for i in range(instate['NRHO'][0])          ]

    if any(imas_data['sources']['pellet']['si_pellet']):
       instate['SE_PELLET'] = [round(float(i*1.0e-19),7) for i in (imas_data['sources']['pellet']['si_pellet']         )]
    else:
       instate['SE_PELLET'] = [round(0.0,7) for i in range(instate['NRHO'][0])          ]

   #if any(imas_data['sources']['pellet']['si_pellet']):
   #   instate['SI_PELLET'] = [round(float(i*1.0e-19),7) for i in (imas_data['sources']['pellet']['si_pellet']         )]
   #else:
   #   instate['SI_PELLET'] = [round(0.0,7) for i in range(instate['NRHO'][0])          ]

   #instate['TORQUE_NB']     = [round(i,7) for i in imas_data['storqueb']['data']           ]
   #instate['TORQUE_IN']     = [round(0.0,7) for i in range(instate['NRHO'][0])          ]

    instate['PE_IONIZATION'] = [round(0.0,7) for i in range(instate['NRHO'][0])          ]
    instate['PI_IONIZATION'] = [round(0.0,7) for i in range(instate['NRHO'][0])          ]
    instate['SE_IONIZATION'] = [round(0.0,7) for i in range(instate['NRHO'][0])          ]
    instate['SI_IONIZATION'] = [round(0.0,7) for i in range(instate['NRHO'][0])          ]

    instate['DENSITY_BEAM']  = [round(float(i*1.0e-19),7) for i in (imas_data['species']['tot_nnbi'])]
    instate['DENSITY_ALPHA'] = [round(float(i*1.0e-19),7) for i in (imas_data['species']['tot_nfus'])]

   #if len(imas_data['species']['pbeam_par']) > 0 and len(imas_data['species']['pbeam_per']) > 0:
   #   WBEAM1                   = [round(float(i*1.602e3),7) for i in imas_data['species']['pbeam_par']]
   #   WBEAM2                   = [round(float(i*1.602e3),7) for i in imas_data['species']['pbeam_per']]
   #   instate['WBEAM']         = [(i+j)*z for (i,j,z) in zip(WBEAM1,WBEAM2,instate['DENSITY_BEAM'])]

   #if len(imas_data['species']['pbeam_par']) > 0 and len(imas_data['species']['pbeam_per']) > 0:
   #   WALPHA1                  = [round(float(i*1.602e3),7) for i in imas_data['species']['pbeam_par']]
   #   WALPHA2                  = [round(float(i*1.602e3),7) for i in imas_data['species']['pbeam_per']]
   #   instate['WALPHA']        = [(i+j)*z for (i,j,z) in zip(WALPHA1,WALPHA2,instate['DENSITY_ALPHA'])]

   #print(instate['WALPHA'])

    if instate['NRHO'][0] != 101:
        old_rho  = instate['RHO']
        new_nrho = 101
        new_rho  = numpy.linspace(0.0,1.0,new_nrho)

        instate['NRHO'         ] = [101]
        instate['RHO'          ] = [round(float(i),7) for i in new_rho                                               ]
       #instate['PSIPOL'       ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['PSIPOL'       ])]
        instate['NE'           ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['NE'           ])]
        instate['NI'           ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['NI'           ])]
       #instate['NZ'           ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['NZ'           ])]
        instate['TE'           ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['TE'           ])]
        instate['TI'           ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['TI'           ])]
       #instate['TZ'           ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['TZ'           ])]

        instate['ZEFF'         ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['ZEFF'         ])]
        instate['OMEGA'        ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['OMEGA'        ])]

        instate['Q'            ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['Q'            ])]
        instate['P_EQ'         ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['P_EQ'         ])]
       #instate['PPRIME'       ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['PPRIME'       ])]
       #instate['FFPRIME'      ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['FFPRIME'      ])]


        PSI    = instate['PSI_BDRY'][0]-instate['PSI_AXIS'][0]
        PSI   *= numpy.arange(instate['NRHO'][0])/(instate['NRHO'][0]-1.0)
        PSIN   = (PSI-PSI[0])/(PSI[-1]-PSI[0])
        RHOPSI = numpy.sqrt(PSIN)
        instate['RHOPSI'       ] = [round(float(i),7) for i in RHOPSI                                                ]

        instate['J_OH'         ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['J_OH'         ])]
        instate['J_NB'         ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['J_NB'         ])]
        instate['J_BS'         ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['J_BS'         ])]
        instate['J_EC'         ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['J_EC'         ])]
        instate['J_IC'         ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['J_IC'         ])]
        instate['J_LH'         ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['J_LH'         ])]
        instate['J_TOT'        ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['J_TOT'        ])]

        instate['PE_NB'        ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['PE_NB'        ])]
        instate['PE_EC'        ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['PE_EC'        ])]
        instate['PE_LH'        ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['PE_LH'        ])]
        instate['PI_NB'        ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['PI_NB'        ])]
        instate['PI_IC'        ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['PI_IC'        ])]
        instate['PI_LH'        ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['PI_LH'        ])]

        instate['P_EI'         ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['P_EI'         ])]
        instate['P_RAD'        ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['P_RAD'        ])]
        instate['P_OHM'        ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['P_OHM'        ])]
        instate['PI_CX'        ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['PI_CX'        ])]
        instate['PI_FUS'       ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['PI_FUS'       ])]
        instate['PE_FUS'       ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['PE_FUS'       ])]

        instate['SE_NB'        ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['SE_NB'        ])]
       #instate['SI_NB'        ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['SI_NB'        ])]
        instate['SE_PELLET'    ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['SE_PELLET'    ])]
#       instate['SI_PELLET'    ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['SI_PELLET'    ])]

#       instate['WBEAM'        ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['WBEAM'        ])]
#       instate['WALPHA'       ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['WALPHA'       ])]

       #instate['TORQUE_NB'    ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['TORQUE_NB'    ])]
       #instate['TORQUE_IN'    ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['TORQUE_IN'    ])]

        instate['SE_IONIZATION'] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['SE_IONIZATION'])]
        instate['SI_IONIZATION'] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['SI_IONIZATION'])]
        instate['PE_IONIZATION'] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['PE_IONIZATION'])]
        instate['PI_IONIZATION'] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['PI_IONIZATION'])]

        instate['DENSITY_BEAM' ] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['DENSITY_BEAM' ])]
        instate['DENSITY_ALPHA'] = [round(float(i),7) for i in numpy.interp(new_rho,old_rho,instate['DENSITY_ALPHA'])]


    instate['NBDRY'] = [numpy.size(imas_data['equilibrium']['rbdry'])]
    NBDRYmax = 85
    NBDRY = numpy.size(imas_data['equilibrium']['rbdry'])
    if NBDRY > NBDRYmax:
       RBDRY = imas_data['equilibrium']['rbdry']
       ZBDRY = imas_data['equilibrium']['zbdry']
       BDRY = zip(RBDRY,ZBDRY)
       BDRYINDS = sorted(random.sample(range(1,NBDRY),NBDRYmax))
       instate['NBDRY'] = [NBDRYmax]
       instate['RBDRY'] = [round(i,7) for i in RBDRY[BDRYINDS]]
       instate['RBDRY'].insert(0, round(imas_data['equilibrium']['rbdry'][0],7))
       instate['RBDRY'].insert(-1,round(imas_data['equilibrium']['rbdry'][-1],7))
       instate['ZBDRY'] = [round(i,7) for i in ZBDRY[BDRYINDS]]
       instate['ZBDRY'].insert(0, round(imas_data['equilibrium']['zbdry'][0],7))
       instate['ZBDRY'].insert(-1,round(imas_data['equilibrium']['zbdry'][-1],7))
    else:
       instate['NBDRY'] = [numpy.size(imas_data['equilibrium']['rbdry'])]
       instate['RBDRY'] = [round(i,7) for i in imas_data['equilibrium']['rbdry']]
       instate['ZBDRY'] = [round(i,7) for i in imas_data['equilibrium']['zbdry']]


   #if type(imas_data['equilibrium']['rgrid']) != type(None):
   #    if LIMITER_MODEL == 1:
   #       NLIMTmax = 86
   #       NLIMT = numpy.size(imas_data['equilibrium']['rgrid'])
   #       if NLIMT > NLIMTmax:
   #          RLIMT = imas_data['equilibrium']['rgrid']
   #          ZLIMT = imas_data['equilibrium']['zgrid']
   #          stride = int(NLIMT / (NLIMTmax+1))
   #          indexes = list(range(2,NLIMTmax-2,stride))
   #          indexes.insert(0,0)
   #          indexes.append(NLIMTmax)
   #          instate['NLIM'] = [len(indexes)]
   #          instate['RLIM'] = [round(RLIMT[i],7) for i in indexes]
   #          instate['ZLIM'] = [round(ZLIMT[i],7) for i in indexes]
   #       else:
   #          instate['NLIM']  = [numpy.size(imas_data['equilibrium']['rgrid'])]
   #          instate['RLIM']  = [round(i,7) for i in imas_data['equilibrium']['rgrid'] ]
   #          instate['ZLIM']  = [round(i,7) for i in imas_data['equilibrium']['zgrid'] ]

   #    elif LIMITER_MODEL == 2:
   #       RLIM_MAX = max(imas_data['equilibrium']['rgrid'])
   #       RLIM_MIN = min(imas_data['equilibrium']['rgrid'])
   #       ZLIM_MAX = max(imas_data['equilibrium']['zgrid'])
   #       ZLIM_MIN = min(imas_data['equilibrium']['zgrid'])
   #       instate['RLIM'] = [RLIM_MAX, RLIM_MIN, RLIM_MIN, RLIM_MAX, RLIM_MAX]
   #       instate['ZLIM'] = [ZLIM_MAX, ZLIM_MAX, ZLIM_MIN, ZLIM_MIN, ZLIM_MAX]
   #       instate['NLIM'] = [len(instate['RLIM'])]
   #else:
   #    RLIM_MAX = max(instate['RBDRY']) + 0.10
   #    RLIM_MIN = min(instate['RBDRY']) - 0.10
   #    ZLIM_MAX = max(instate['ZBDRY']) + 0.10
   #    ZLIM_MIN = min(instate['ZBDRY']) - 0.10
   #    instate['RLIM'] = [RLIM_MAX, RLIM_MIN, RLIM_MIN, RLIM_MAX, RLIM_MAX]
   #    instate['ZLIM'] = [ZLIM_MAX, ZLIM_MAX, ZLIM_MIN, ZLIM_MIN, ZLIM_MAX]
   #    instate['NLIM'] = [len(instate['RLIM'])]

    RLIM_MAX = max(instate['RBDRY']) + 0.10
    RLIM_MIN = min(instate['RBDRY']) - 0.10
    ZLIM_MAX = max(instate['ZBDRY']) + 0.10
    ZLIM_MIN = min(instate['ZBDRY']) - 0.10
    instate['RLIM'] = [RLIM_MAX, RLIM_MIN, RLIM_MIN, RLIM_MAX, RLIM_MAX]
    instate['ZLIM'] = [ZLIM_MAX, ZLIM_MAX, ZLIM_MIN, ZLIM_MIN, ZLIM_MAX]
    instate['NLIM'] = [len(instate['RLIM'])]

    limit_instate_size =  min(instate['NRHO'][0],instate['NLIM'][0],instate['NBDRY'][0])
    instate_var_names = list(instate.keys())
    for ivar in instate_var_names:
        if   len(instate[ivar]) >= limit_instate_size:
             if all(item == 0 for item in instate[ivar]): del instate[ivar]
        elif type(instate[ivar][0]) == type_none:         del instate[ivar]

    INSTATE = Namelist()
    INSTATE['instate'] = {}
    INSTATE['instate'].update(instate)
    INSTATE.write("instate_%s_%s.%s" % (TOKAMAK_ID,SHOT_ID,TIME_ID))

    return instate,imas_data


if __name__ == "__main__":
   import matplotlib.pyplot as plt
  #fig,axs = plt.subplots(nrows=2,ncols=5,figsize=(8,6),dpi=200)

#  fpaths = ["iter_reference_scenarios_0725/3/"]
   fpaths = ["iter_reference_scenarios_0725/3/","iter_reference_scenarios_0725/4/"]
#  fnames = ["core_profiles.h5", "core_sources.h5", "core_transport.h5", "equilibrium.h5", "master.h5", "ntms.h5", "summary.h5"]

   for fpath in fpaths:
      #imas_data = read_imas_data(fpath=fpath)
       instate_data,imas_data = to_instate(fpath=fpath)
       continue

      #fig = plt.figure("figure",dpi=200)
      #axs = fig.add_subplot(111)
      #axs.plot(instate_data['RHO'],instate_data['NE'],label="electrons")
      #NIONS = [float(i+j+k+m) for (i,j,k,m) in zip(instate_data['NI'],instate_data['NZ'],instate_data['DENSITY_BEAM'],instate_data['DENSITY_ALPHA'])]
      #axs.plot(instate_data['RHO'],NIONS,label="ions")
      #fig.legend()
      #plt.show()
      #plt.close()

      #axs[0,0].plot(instate_data['RHO'],instate_data['TE'])
      #axs[0,1].plot(instate_data['RHO'],instate_data['TI'])
      #axs[0,2].plot(instate_data['RHO'],instate_data['NE'])
      #axs[0,3].plot(instate_data['RHO'],[abs(i*1.0e-3) for i in instate_data['OMEGA']])
      #axs[0,4].plot(instate_data['RHO'],instate_data['Q'])

      #axs[1,0].plot(instate_data['RHO'],instate_data['PE_EC'])
      #axs[1,1].plot(instate_data['RHO'],instate_data['PE_NB'])
      #axs[1,1].plot(instate_data['RHO'],instate_data['PI_NB'])
      #axs[1,2].plot(instate_data['RHO'],instate_data['SI_PLT'])
      #axs[1,2].plot(instate_data['RHO'],[i*100 for i in instate_data['DENSITY_BEAM']])
      #axs[1,3].plot(instate_data['RHO'],instate_data['J_NB'])
      #axs[1,3].plot(instate_data['RHO'],instate_data['J_EC'])
      #axs[1,4].plot(instate_data['RBDRY'],instate_data['ZBDRY'])

      #for ind in range(len(imas_data['equilibrium']['q'])):
      #    print(imas_data['equilibrium']['rho_tor_norm'][ind],imas_data['equilibrium']['q'][ind])
      #print()

       q_min_shift = 1.1 - min(imas_data['equilibrium']['q'])

       shot_id = instate_data['TIME_ID'][0]
       fig = plt.figure("figure",dpi=200)
       axs = fig.add_subplot(111)
       axs.plot(imas_data['equilibrium']['rho_tor_norm'],imas_data['equilibrium']['q'],               label='$q$(original)')
       axs.plot(imas_data['equilibrium']['rho_tor_norm'],imas_data['equilibrium']['q'] + q_min_shift, label='$q$(shifted)')
       axs.plot(imas_data['equilibrium']['rho_tor_norm'],imas_data['equilibrium']['magnetic_shear'],  label='$\\hat{s}$')
       axs.set_title("Safety Factor and Magnetic Shear for %s" % shot_id)
       axs.set_xlabel("$\\rho$")
       axs.set_ylabel("$q$,$\\hat{s}$")
       axs.hlines(y=1.0,xmin=0.0,xmax=1.0,linestyle='--',color='k')
       axs.legend()
       plt.show()
       plt.close()




