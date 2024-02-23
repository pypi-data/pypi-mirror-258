<p align="center">
  <a href="https://polymer-molecular-dynamics.netlify.app/"><img src="https://github.com/kevinshen56714/Polymer-Molecular-Dynamics/raw/main/website/static/img/logo-with-text.svg" alt="PMD" width="450rem"></a>
</p>
<p align="center">
    <em>Polymer Molecular Dynamics toolkit, easy to learn, fast to code, ready for polymer property production</em>
</p>
<p align="center">
<a href="https://github.com/kevinshen56714/Polymer-Molecular-Dynamics/actions/workflows/main.yml/badge.svg?event=push" target="_blank">
    <img src="https://github.com/kevinshen56714/Polymer-Molecular-Dynamics/actions/workflows/main.yml/badge.svg?event=push" alt="GitHub Workflow">
</a>
<a href="https://coveralls.io/github/kevinshen56714/Polymer-Molecular-Dynamics" target="_blank">
    <img src="https://coveralls.io/repos/github/kevinshen56714/Polymer-Molecular-Dynamics/badge.svg?service=github" alt="Coverage">
</a>
<a href="https://pypi.python.org/pypi/pmd" target="_blank">
    <img src="http://img.shields.io/pypi/v/pmd.svg" alt="Package version">
</a>
<a href="https://pypi.org/project/pmd" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/pmd" alt="Supported Python versions">
</a>
<a href="https://pepy.tech/project/pmd" target="_blank">
    <img src="https://pepy.tech/badge/pmd" alt="Package download">
</a>
</p>

---

**Documentation**: <a href="https://polymer-molecular-dynamics.netlify.app" target="_blank">https://polymer-molecular-dynamics.netlify.app</a>

**Source Code**: <a href="https://github.com/kevinshen56714/Polymer-Molecular-Dynamics" target="_blank">https://github.com/kevinshen56714/Polymer-Molecular-Dynamics</a>

---

PMD is a modern, fast, python framework for building LAMMPS input and data files for predicting polymer properties

The key properties are:

- **Glass transition temperature (Tg)** - [[Guide](http://polymer-molecular-dynamics.netlify.app/docs/guides/glass-transition-temperature)] [[Scripts](https://github.com/kevinshen56714/Polymer-Molecular-Dynamics/tree/main/scripts/Tg)]
- **Gas diffusivity** - [[Guide](http://polymer-molecular-dynamics.netlify.app/docs/guides/gas-diffusivity)] [[Scripts](https://github.com/kevinshen56714/Polymer-Molecular-Dynamics/tree/main/scripts/Gas_diffusivity)]
- **Solvent diffusivity** - [[Guide](http://polymer-molecular-dynamics.netlify.app/docs/guides/solvent-diffusivity)] [[Scripts](https://github.com/kevinshen56714/Polymer-Molecular-Dynamics/tree/main/scripts/Solvent_diffusivity)]
- **Viscosity** - [[Guide](https://polymer-molecular-dynamics.netlify.app/docs/guides/viscosity)] [[Scripts](https://github.com/kevinshen56714/Polymer-Molecular-Dynamics/tree/main/scripts/Shear_deformation)]
- **Young's modulus** and **tensile strengths** - [[Guide](https://polymer-molecular-dynamics.netlify.app/docs/guides/mechanical-properties)] [[Scripts](https://github.com/kevinshen56714/Polymer-Molecular-Dynamics/tree/main/scripts/Tensile_deformation)]
- **Thermal conductivity** - [[Scripts](https://github.com/kevinshen56714/Polymer-Molecular-Dynamics/tree/main/scripts/HeatFluxMeasurement)]

## Installation

```bash
pip install pmd
```

## Example

Below are examples of using PMD to generate LAMMPS data and input files:

### From the command line

```bash
pmd-template
```
https://github.com/kevinshen56714/Polymer-Molecular-Dynamics/assets/11501902/ba892b38-d735-4109-bb66-e4bd7b967245

### From a python script

#### example.py

```python
import pmd

# A list of polymer SMILES strings to create simulations for
smiles_list = ['*CC*', '*CC(*)CC', '*CC(*)CCCC', '*CC(*)c1ccccc1']

for smiles in smiles_list:
    # Define polymer and system specs
    syst = pmd.System(smiles=smiles,
                      density=0.8,
                      natoms_total=5000,
                      natoms_per_chain=150,
                      builder=pmd.EMC(force_field='pcff'))

    # Customize LAMMPS simulation
    lmp = pmd.Lammps(read_data_from=syst,
                     procedures=[
                         pmd.Minimization(min_style='cg'),
                         pmd.Equilibration(Teq=600, Tmax=800),
                         pmd.TgMeasurement(Tinit=600, Tfinal=200)
                     ])

    # Create job scheduler settings
    job = pmd.Torque(run_lammps=lmp,
                     jobname=smiles,
                     project='Your-project-id',
                     nodes=2,
                     ppn=24,
                     walltime='48:00:00')

    # Generate all necessary files at each SMILES folder
    run = pmd.Pmd(system=syst, lammps=lmp, job=job)
    run.create(output_dir=smiles, save_config=True)
```

### From a YAML file

PMD can generate config file in YAML format out of the box, which helps you keep track of all the parameters used for each simulation. At the same time, you can build PMD systems directly via the config file from the command line. For example, run the `pmd-load` command with the following `config.yaml` to get exact same setup as the above example python script (but only for '\*CC\*').

```bash
$ pmd-load config.yaml [-o output_dir]
```

#### config.yaml

```yaml
pmd.System:
  smiles: "*CC*"
  density: 0.8
  builder:
    pmd.EMC:
      force_field: pcff
  natoms_total: 5000
  natoms_per_chain: 150
  data_fname: data.lmps
pmd.Lammps:
  read_data: data.lmps # This file name has to match data_fname if build from a yaml file
  get_functional_form_from: # A PMD Builder has to be provided if build from a yaml file
    pmd.EMC:
      force_field: pcff
  procedures:
    - pmd.Minimization:
        min_style: cg
    - pmd.Equilibration:
        Teq: 600
        Tmax: 800
    - pmd.TgMeasurement:
        Tinit: 600
        Tfinal: 200
  lmp_input_fname: lmp.in
pmd.Torque:
  run_lammps: lmp.in # This file name has to match the above lmp_input_fname if build from a yaml file
  jobname: "*CC*"
  project: Your-project-id
  nodes: 2
  ppn: 24
  walltime: "48:00:00"
  job_fname: job.pbs
```
