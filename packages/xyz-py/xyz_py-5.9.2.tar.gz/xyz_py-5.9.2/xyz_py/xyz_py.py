#! /usr/bin/env python3

'''
This is the main part of xyz_py
'''

import numpy as np
import numpy.typing as npt
import numpy.linalg as la
from ase import neighborlist, Atoms
from ase.geometry.analysis import Analysis
import copy
import re
import scipy.optimize as spo
import sys
from collections import defaultdict
import deprecation

from . import version
from . import atomic

__version__ = version.__version__


def load_xyz(f_name: str, atomic_numbers: bool = False,
             add_indices: bool = False,
             capitalise: bool = True) -> tuple[list, npt.NDArray]:
    '''
    Load labels and coordinates from a .xyz file

    File assumes two header lines, first containing number of atoms
    and second containing a comment or blank, followed by actual data

    Parameters
    ----------
    f_name: str
        File name
    atomic_numbers: bool, default False
        If True, reads xyz file with atomic numbers and converts to labels
    add_indices: bool, default False
        If True, add indices to atomic labels
        (replacing those which may exist already)
    capitalise: bool, default True
        If True, capitalise atomic labels

    Returns
    -------
    list
        atomic labels
    np.ndarray
        (n_atoms,3) array containing xyz coordinates of each atom
    '''

    # Check xyz file formatting
    check_xyz(f_name)

    if atomic_numbers:
        _numbers = np.loadtxt(
            f_name, skiprows=2, usecols=0, dtype=int, ndmin=1
        )
        _labels = num_to_lab(_numbers.tolist())
    else:
        _labels = np.loadtxt(f_name, skiprows=2, usecols=0, dtype=str, ndmin=1)
        _labels = _labels.tolist()

    # Set labels as capitals
    if capitalise:
        _labels = [lab.capitalize() for lab in _labels]

    if add_indices:
        _labels = remove_label_indices(_labels)
        _labels = add_label_indices(_labels)

    _coords = np.loadtxt(f_name, skiprows=2, usecols=(1, 2, 3), ndmin=2)

    return _labels, _coords


def load_xyz_comment(f_name: str) -> str:
    '''
    Load comment line from an xyz file

    Parameters
    ----------
    f_name: str
        File name

    Returns
    -------
    str
        comment line of xyz file
    '''

    # Check xyz file formatting
    check_xyz(f_name)

    with open(f_name, 'r') as f:
        next(f)
        comment = next(f)

    comment = comment.rstrip()

    return comment


def check_xyz(f_name: str) -> None:
    '''
    Checks if .xyz file has correct length and contains two header lines
    for the number of atoms and an optional comment

    Parameters
    ----------
    f_name: str
        File name

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the .xyz file has incorrect length, or is missing the number
        of atoms and comment lines
    '''

    # Check file contains number of atoms on first line
    with open(f_name, 'r') as f:
        line = next(f)
        if len(line.split()) != 1:
            raise ValueError('.xyz file does not contain number of atoms')
        else:
            try:
                n_atoms = int(line)
            except ValueError:
                raise ValueError('.xyz file number of atoms is malformed')

            n_lines = len(f.readlines()) + 1  # + 1 for next
            if n_atoms + 2 != n_lines:
                raise ValueError('.xyz file length/format is incorrect')

    return


def save_xyz(f_name: str, labels: list, coords: np.ndarray,
             with_numbers: bool = False, verbose: bool = True,
             mask: list = [], atomic_numbers: bool = False,
             comment: str = '') -> None:
    '''
    Save an xyz file containing labels and coordinates

    Parameters
    ----------
    f_name: str
        File name
    labels: list
        atomic labels
    coords: np.ndarray
        list of 3 element lists containing xyz coordinates of each atom
    with_numbers: bool, default False
        If True, add/overwrite numbers to labels before printing
    verbose: bool, default True
        Print information on filename to screen
    mask: list, optional
        n_atom list of 0 (exclude) and 1 (include) indicating which
        atoms to print
    atomic_numbers: bool, default False
        If True, will save xyz file with atomic numbers
    comment: str, default ''
        Comment line printed to 2nd line of .xyz file

    Returns
    -------
    None
    '''

    # Option to have numbers added
    if with_numbers:
        # Remove and re-add numbers to be safe
        _labels = remove_label_indices(labels)
        _labels = add_label_indices(_labels)
    else:
        _labels = labels

    # Set up masks
    if mask:
        coords = np.delete(coords, mask, axis=0)
        _labels = np.delete(_labels, mask, axis=0).tolist()

    n_atoms = len(_labels)

    if atomic_numbers:
        _labels = remove_label_indices(_labels)
        _numbers = lab_to_num(_labels)
        _identifier = _numbers
    else:
        _identifier = _labels

    with open(f_name, 'w') as f:
        f.write(f'{n_atoms:d}\n')
        f.write(f'{comment}')
        for ident, trio in zip(_identifier, coords):
            f.write('\n{:5} {:15.7f} {:15.7f} {:15.7f}'.format(ident, *trio))

    if verbose:
        print('New xyz file written to {}'.format(f_name))

    return


def remove_label_indices(labels):
    '''
    Remove label indexing from atomic symbols
    indexing is either numbers or numbers followed by letters:
    e.g. H1, H2, H3
    or H1a, H2a, H3a

    Parameters
    ----------
    labels: list
        atomic labels

    Returns
    -------
    list
        atomic labels without indexing
    '''

    labels_nn = []
    for label in labels:
        no_digits = []
        for i in label:
            if not i.isdigit():
                no_digits.append(i)
            elif i.isdigit():
                break
        result = ''.join(no_digits)
        labels_nn.append(result)

    return labels_nn


def add_label_indices(labels, style='per_element', start_index=1):
    '''
    Add label indexing to atomic symbols - either element or per atom.

    Parameters
    ----------
    labels: list
        atomic labels
    style: str, optional
        {'per_element', 'sequential'}
            'per_element': Index by element e.g. Dy1, Dy2, N1, N2, etc.
            'sequential': Index the atoms 1->N regardless of element
    start_index: int
        integer at which indexing will start

    Returns
    -------
    list
        atomic labels with indexing
    '''

    # remove numbers just in case
    labels_nn = remove_label_indices(labels)

    # Just number the atoms 1->N regardless of element
    if style == 'sequential':
        labels_wn = ['{}{:d}'.format(lab, it + start_index)
                     for (it, lab) in enumerate(labels_nn)]

    # Index by element Dy1, Dy2, N1, N2, etc.
    if style == 'per_element':
        # Get list of unique elements
        atoms = set(labels_nn)
        # Create dict to keep track of index of current atom of each element
        atom_count = {atom: start_index for atom in atoms}
        # Create labelled list of elements
        labels_wn = []

        for lab in labels_nn:
            # Index according to dictionary
            labels_wn.append('{}{:d}'.format(lab, atom_count[lab]))
            # Then add one to dictionary
            atom_count[lab] += 1

    return labels_wn


def count_n_atoms(form_str):
    '''
    Count number of atoms in a chemical formula

    Parameters
    ----------
    form_str: str
        chemical formula string

    Returns
    -------
    int
        number of atoms in chemical formula
    '''

    form_dict = formstr_to_formdict(form_str)

    n_atoms = sum(form_dict.values())

    return n_atoms


def index_elements(labels, shift=0):
    '''
    Return dictionary of element (keys) and indices (values) from list
    of labels

    Parameters
    ----------
    labels: list
        atomic labels
    shift: int, optional
        additive shift to apply to all indices

    Returns
    -------
    dict
        element (keys) and indices (values)
    '''

    labels_nn = remove_label_indices(labels)

    ele_index = {}

    for it, lab in enumerate(labels_nn):
        try:
            ele_index[lab].append(it + shift)
        except KeyError:
            ele_index[lab] = [it + shift]

    return ele_index


def count_elements(labels):
    '''
    Count number of each element in a list of elements

    Parameters
    ----------
    labels: list
        atomic labels
    Returns
    -------
    dict
        dictionary of elements (keys) and counts (vals)
    '''

    labels_nn = remove_label_indices(labels)

    ele_count = {}

    for lab in labels_nn:
        try:
            ele_count[lab] += 1
        except KeyError:
            ele_count[lab] = 1

    return ele_count


def get_formula(labels):
    '''
    Generates empirical formula in alphabetical order given a list of labels

    Parameters
    ----------
    labels: list
        atomic labels
    Returns
    -------
    str
        Empirical formula in alphabetical order
    '''

    formdict = count_elements(labels)

    formula = formdict_to_formstr(formdict)

    return formula


def formstr_to_formdict(form_str):
    '''
    Converts formula string into dictionary of {atomic label:quantity} pairs

    Parameters
    ----------
    form_string: str
        Chemical formula as string

    Returns
    -------
    dict
        dictionary of {atomic label:quantity} pairs
    '''

    form_dict = {}
    # Thanks stack exchange!
    s = re.sub
    f = s(
        "[()',]",
        '',
        str(
            eval(
                s(
                    r',?(\d+)',
                    r'*\1,',
                    s(
                        '([A-Z][a-z]*)',
                        r'("\1",),',
                        form_str
                    )
                )
            )
        )
    ).split()
    for c in set(f):
        form_dict[c] = f.count(c)

    return form_dict


def formdict_to_formstr(form_dict, include_one=False):
    '''
    Converts dictionary of {atomic label:quantity} pairs into
    a single formula string in alphabetical order

    Parameters
    ----------
    form_dict: dict
        dictionary of {atomic label:quantity} pairs
    include_one: bool, default False
        Include 1 in final chemical formula e.g. C1H4

    Returns
    -------
    str
        Chemical formula as string in alphabetical order
    '''

    # Formula labels and quantities as separate lists with same order
    form_labels = ['{:s}'.format(key) for key in form_dict.keys()]
    form_quants = [val for val in form_dict.values()]

    # Quantities of each element as a string
    if include_one:
        form_quants_str = ['{:d}'.format(quant)
                           for quant in form_quants]
    else:
        form_quants_str = ['{:d}'.format(quant)
                           if quant > 1 else ''
                           for quant in form_quants]

    # Sort labels in alphabetical order
    order = np.argsort(form_labels).tolist()
    form_labels_o = [form_labels[o] for o in order]
    # Use same ordering for quantities
    form_quants_str_o = [form_quants_str[o] for o in order]

    # Make list of elementquantity strings
    form_list = [el + quant
                 for el, quant in zip(form_labels_o, form_quants_str_o)]

    # Join strings together into empirical formula
    form_string = ''.join(form_list)

    return form_string


def contains_metal(form_string):
    '''
    Indicates if a metal is found in a chemical formula string

    Parameters
    ----------
    form_string: str
        Chemical formula as string

    Returns
    -------
    bool
        True if metal found, else False
    '''
    metal_found = False

    for metal in atomic.metals:
        if metal in form_string:
            metal_found = True
            break

    return metal_found


def combine_xyz(labels_1, labels_2, coords_1, coords_2):
    '''
    Combine two sets of labels and coordinates

    Parameters
    ----------
    labels_1: list
        Atomic labels
    coords_1: list
        xyz coordinates as (n_atoms, 3) array
    labels_2: list
        Atomic labels
    coords_2: list
        xyz coordinates as (n_atoms, 3) array

    Returns
    -------
    list
        Combined atomic labels
    np.ndarray
        Combined xyz coordinates as (n_atoms, 3) array
    '''

    # Concatenate labels lists
    labels = labels_1 + labels_2

    # Concatenate coordinate lists
    coords = coords_1 + coords_2

    return labels, coords


def get_neighborlist(labels, coords, adjust_cutoff={}):
    '''
    Calculate ASE neighbourlist based on covalent radii

    Parameters
    ----------
    labels: list
        Atomic labels
    coords: np.ndarray
        xyz coordinates as (n_atoms, 3) array
    adjust_cutoff: dict, optional
        dictionary of atoms (keys) and new cutoffs (values)

    Returns
    -------
    ASE neighbourlist object
        Neighbourlist for system
    '''

    # Remove labels if present
    labels_nn = remove_label_indices(labels)

    # Load molecule
    mol = Atoms(''.join(labels_nn), positions=coords)

    # Define cutoffs for each atom using atomic radii
    cutoffs = neighborlist.natural_cutoffs(mol)

    # Modify cutoff if requested
    if adjust_cutoff:
        for it, label in enumerate(labels_nn):
            if label in adjust_cutoff.keys():
                cutoffs[it] = adjust_cutoff[label]

    # Create neighbourlist using cutoffs
    neigh_list = neighborlist.NeighborList(
        cutoffs=cutoffs,
        self_interaction=False,
        bothways=True
    )

    # Update this list by specifying the atomic positions
    neigh_list.update(mol)

    return neigh_list


def get_adjacency(labels, coords, adjust_cutoff={}):
    '''
    Calculate adjacency matrix using ASE based on covalent radii.

    Parameters
    ----------
    labels: list
        Atomic labels
    coords: np.ndarray
        xyz coordinates as (n_atoms, 3) array
    adjust_cutoff: dict, optional
        dictionary of atoms (keys) and new cutoffs (values)
    save: bool, default False
        If True save to file given by `f_name`
    f_name: str, default 'adjacency.dat'
        If save true, this name is used for the file containing the adjacency
        matrix

    Returns
    -------
    np.array
        Adjacency matrix with same order as labels/coords
    '''

    # Remove labels if present
    labels_nn = remove_label_indices(labels)

    # Get ASE neighbourlist object
    neigh_list = get_neighborlist(
        labels_nn,
        coords,
        adjust_cutoff=adjust_cutoff
    )

    # Create adjacency matrix
    adjacency = neigh_list.get_connectivity_matrix(sparse=False)

    return adjacency


@deprecation.deprecated(
    deprecated_in='5.3.0', removed_in='6.3.0', current_version=__version__,
    details='Use find_bonds instead'
)
def get_bonds(labels, coords, neigh_list=None, verbose=True, style='indices'):
    '''
    Calculate list of atoms between which there is a bond.
    Using ASE. Only unique bonds are retained.
    e.g. 0-1 and not 1-0

    Parameters
    ----------
    labels: list
        Atomic labels
    coords: np.ndarray
        xyz coordinates as (n_atoms, 3) array in Angstrom
    neigh_list: ASE neighbourlist object, optional
        neighbourlist of system
    f_name: str, 'bonds.dat'
        filename to save bond list to
    save: bool, default False
        Save bond list to file
    verbose: bool, default True
        Print number of bonds to screen
    style: str, {'indices','labels'}
            indices: Bond list contains atom number
            labels : Bond list contains atom label

    Returns
    -------
    list[list[int | str]]
        list of lists of unique bonds (atom pairs)
    '''

    bonds, _ = find_bonds(
        labels, coords, neigh_list=neigh_list, verbose=verbose, style=style
    )

    return bonds


def find_bonds(labels, coords, neigh_list=None, verbose=True, style='labels'):
    '''
    Calculate list of atoms between which there is a bond.
    Using ASE. Only unique bonds are retained.
    e.g. 0-1 and not 1-0

    Parameters
    ----------
    labels: list
        Atomic labels
    coords: np.ndarray
        xyz coordinates as (n_atoms, 3) array in Angstrom
    neigh_list: ASE neighbourlist object, optional
        neighbourlist of system
    f_name: str, 'bonds.dat'
        filename to save bond list to
    save: bool, default False
        Save bond list to file
    verbose: bool, default True
        Print number of bonds to screen
    style: str, {'indices','labels'}
            indices: Bond list contains atom number
            labels : Bond list contains atom label

    Returns
    -------
    list[list[int | str]]
        list of lists of unique bonds (atom pairs)
    np.ndarray
        Bond length in Angstrom
    '''

    # Remove labels if present
    labels_nn = remove_label_indices(labels)

    # Create molecule object
    mol = Atoms(''.join(labels_nn), positions=coords)

    # Get neighbourlist if not provided to function
    if not neigh_list:
        neigh_list = get_neighborlist(labels, coords)

    # Get object containing analysis of molecular structure
    ana = Analysis(mol, nl=neigh_list)

    # Get bonds from ASE
    # Returns: list of lists of lists containing UNIQUE bonds
    # Defined as
    # Atom 1: [bonded atom, bonded atom], ...
    # Atom 2: [bonded atom, bonded atom], ...
    # Atom n: [bonded atom, bonded atom], ...
    # Where only the right hand side is in the list
    is_bonded_to = ana.unique_bonds

    # Remove weird outer list wrapping the entire thing twice...
    is_bonded_to = is_bonded_to[0]
    # Create list of bonds (atom pairs) by appending lhs of above
    # definition to each element of the rhs
    bonds = []
    bonds = [
        [it, atom]
        for it, ibt in enumerate(is_bonded_to)
        for atom in ibt
    ]

    # Count bonds
    n_bonds = len(bonds)

    # Calculate actual values
    values = np.array([
        ana.get_bond_value(0, bond)
        for bond in bonds
    ])

    # Set format and convert to atomic labels if requested
    if style == 'labels':
        bonds = [
            [labels[atom1], labels[atom2]]
            for atom1, atom2 in bonds
        ]
    elif style == 'indices':
        pass
    else:
        sys.exit('Unknown style specified')

    # Print number of bonds to screen
    if verbose:
        print('{:d} bonds'.format(n_bonds))

    return bonds, values


@deprecation.deprecated(
    deprecated_in='5.3.0', removed_in='6.3.0', current_version=__version__,
    details='Use find_angles instead'
)
def get_angles(labels, coords, neigh_list=None, verbose=True, style='indices'):
    '''
    Calculate list of atoms between which there is a bond angle.
    Using ASE. Only unique angles are retained.
    e.g. 0-1-2 but not 2-1-0

    Parameters
    ----------
    labels: list
        Atomic labels
    coords: np.ndarray
        xyz coordinates as (n_atoms, 3) array
    neigh_list: ASE neighbourlist object, optional
        neighbourlist of system
    f_name: str, default 'angles.dat'
        filename to save angle list to
    save: bool, default False
        Save angle list to file
    verbose: bool, default True
        Print number of angles to screen
    style: str, {'indices','labels'}
            indices: Angle list contains atom number
            labels : Angle list contains atom label
            values : Angle list is values in degrees

    Returns
    -------
    list[list[int | str | float]]
        list of lists of unique angles (atom trios)
    '''

    angles, _ = find_angles(
        labels, coords, neigh_list=neigh_list, verbose=verbose, style=style
    )

    return angles


def find_angles(labels, coords, neigh_list=None, verbose=True,
                style='labels'):
    '''
    Calculate all angles using ASE. Only unique angles are retained.
    e.g. 0-1-2 but not 2-1-0

    Parameters
    ----------
    labels: list
        Atomic labels
    coords: np.ndarray
        xyz coordinates as (n_atoms, 3) array
    neigh_list: ASE neighbourlist object, optional
        neighbourlist of system
    f_name: str, default 'angles.dat'
        filename to save angle list to
    save: bool, default False
        Save angle list to file
    verbose: bool, default True
        Print number of angles to screen
    style: str, {'indices','labels'}
            indices: Angle labels are atom number
            labels : Angle labels are atom label

    Returns
    -------
    list[list[int | str]]
        list of lists of unique angles (atom trios) as labels or indices
    np.ndarray
        Angles in degrees
    '''

    # Remove labels if present
    labels_nn = remove_label_indices(labels)

    # Create molecule object
    mol = Atoms(''.join(labels_nn), positions=coords)

    # Get neighbourlist if not provided to function
    if not neigh_list:
        neigh_list = get_neighborlist(labels, coords)

    # Get object containing analysis of molecular structure
    ana = Analysis(mol, nl=neigh_list)

    # Get angles from ASE
    # Returns: list of lists of lists containing UNIQUE angles
    # Defined as
    # Atom 1: [[atom,atom], [atom,atom]], ...
    # Atom 2: [[atom,atom], [atom,atom]], ...
    # Atom n: [[atom,atom], [atom,atom]], ...
    # Where only the right hand side is in the list
    is_angled_to = ana.unique_angles

    # Remove weird outer list wrapping the entire thing twice...
    is_angled_to = is_angled_to[0]
    # Create list of angles (atom trios) by appending lhs of above
    # definition to each element of the rhs
    angles = []
    for it, ibt in enumerate(is_angled_to):
        for atoms in ibt:
            angles.append([it, *atoms])

    # Count angles
    n_angles = len(angles)

    # Calculate actual values
    values = np.array([
        ana.get_angle_value(0, angle)
        for angle in angles
    ])

    # Set format and convert to atomic labels if requested
    if style == 'labels':
        angles = [
            [labels[atom1], labels[atom2], labels[atom3]]
            for atom1, atom2, atom3 in angles
        ]
    elif style == 'indices':
        pass
    else:
        sys.exit('Unknown style specified')

    # Print number of angles to screen
    if verbose:
        print('{:d} angles'.format(n_angles))

    return angles, values


@deprecation.deprecated(
    deprecated_in='5.3.0', removed_in='6.3.0', current_version=__version__,
    details='Use find_dihedrals instead'
)
def get_dihedrals(labels, coords, neigh_list=None, verbose=True,
                  style='indices'):
    '''
    Calculate and list of atoms between which there is a dihedral.
    Using ASE. Only unique dihedrals are retained.
    e.g. 0-1-2-3 but not 3-2-1-0

    Parameters
    ----------
    labels: list
        Atomic labels
    coords: np.ndarray
        xyz coordinates as (n_atoms, 3) array
    neigh_list: ASE neighbourlist object, optional
        neighbourlist of system
    f_name: str, default 'dihedrals.dat'
        filename to save angle list to
    save: bool, default False
        Save angle list to file
    verbose: bool, default True
        Print number of dihedrals to screen
    style: str, {'indices','labels'}
            indices: Dihedral list contains atom number
            labels : Dihedral list contains atom label

    Returns
    -------
    list[list[int | str]]
        list of lists of unique dihedrals (atom quads)
    '''
    dihedrals, _ = find_dihedrals(
        labels, coords, neigh_list=neigh_list, verbose=verbose, style=style
    )

    return dihedrals


def find_dihedrals(labels, coords, neigh_list=None, verbose=True,
                   style='labels'):
    '''
    Calculate and list of atoms between which there is a dihedral.
    Using ASE. Only unique dihedrals are retained.
    e.g. 0-1-2-3 but not 3-2-1-0

    Parameters
    ----------
    labels: list
        Atomic labels
    coords: np.ndarray
        xyz coordinates as (n_atoms, 3) array
    neigh_list: ASE neighbourlist object, optional
        neighbourlist of system
    f_name: str, default 'dihedrals.dat'
        filename to save angle list to
    save: bool, default False
        Save angle list to file
    verbose: bool, default True
        Print number of dihedrals to screen
    style: str, {'indices','labels'}
            indices: Dihedral list contains atom number
            labels : Dihedral list contains atom label

    Returns
    -------
    list[list[int | str]]
        list of lists of unique dihedrals (atom quads)
    np.ndarray
        Dihedral angles in degrees
    '''

    # Remove labels if present
    labels_nn = remove_label_indices(labels)

    # Create molecule object
    mol = Atoms(''.join(labels_nn), positions=coords)

    # Get neighbourlist if not provided to function
    if not neigh_list:
        neigh_list = get_neighborlist(labels, coords)

    # Get object containing analysis of molecular structure
    ana = Analysis(mol, nl=neigh_list)

    # Get dihedrals from ASE
    # Returns: list of lists of lists containing UNIQUE dihedrals
    # Defined as
    # Atom 1: [[atom,atom,atom], [atom,atom,atom]], ...
    # Atom 2: [[atom,atom,atom], [atom,atom,atom]], ...
    # Atom n: [[atom,atom,atom], [atom,atom,atom]], ...
    # Where only the right hand side is in the list
    is_dihedraled_to = ana.unique_dihedrals

    # Remove weird outer list wrapping the entire thing twice...
    is_dihedraled_to = is_dihedraled_to[0]
    # Create list of dihedrals (atom quads) by appending lhs of above
    # definition to each element of the rhs
    dihedrals = []
    for it, ibt in enumerate(is_dihedraled_to):
        for atoms in ibt:
            dihedrals.append([it, *atoms])

    # Calculate actual values
    values = np.array([
        ana.get_dihedral_value(0, dihedral)
        for dihedral in dihedrals
    ])

    # Count dihedrals
    n_dihedrals = len(dihedrals)

    # Set format and convert to atomic labels if requested
    if style == 'labels':
        dihedrals = [
            [
                labels[atom1],
                labels[atom2],
                labels[atom3],
                labels[atom4]
            ]
            for atom1, atom2, atom3, atom4 in dihedrals
        ]
    elif style == 'indices':
        pass
    else:
        sys.exit('Unknown style specified')

    # Print number of dihedrals to screen
    if verbose:
        print('{:d} dihedrals'.format(n_dihedrals))

    return dihedrals, values


def lab_to_num(labels):
    '''
    Convert atomic label to atomic number

    Parameters
    ----------
    labels: list[str]
        Atomic labels

    Returns
    -------
    list[int]
        Atomic numbers
    '''

    labels_nn = remove_label_indices(labels)

    numbers = [atomic.lab_num[lab] for lab in labels_nn]

    return numbers


def num_to_lab(numbers, numbered=True):
    '''
    Convert atomic number to atomic labels

    Parameters
    ----------
    numbers: list[int]
        Atomic numbers
    numbered: bool, optional
        Add indexing number to end of atomic labels

    Returns
    -------
    list[str]
        Atomic labels
    '''

    labels = [atomic.num_lab[num] for num in numbers]

    if numbered:
        labels_wn = add_label_indices(labels)
    else:
        labels_wn = labels

    return labels_wn


def reflect_coords(coords):
    '''
    Reflect coordinates through xy plane

    Parameters
    ----------
    coords: np.ndarray
        xyz coordinates as (n_atoms, 3) array

    Returns
    -------
    np.ndarray
        xyz coordinates as (n_atoms, 3) array

    '''

    # Calculate normal to plane
    x = [1, 0, 0]
    y = [0, 1, 0]
    normal = np.cross(x, y)

    # Set up transformation matrix
    # https://en.wikipedia.org/wiki/Transformation_matrix#Reflection_2
    trans_mat = np.zeros([3, 3])

    trans_mat[0, 0] = 1. - 2. * normal[0] ** 2.
    trans_mat[1, 0] = -2. * normal[0] * normal[1]
    trans_mat[2, 0] = -2. * normal[0] * normal[2]
    trans_mat[0, 1] = -2. * normal[0] * normal[1]
    trans_mat[1, 1] = 1. - 2. * normal[1] ** 2.
    trans_mat[2, 1] = -2. * normal[1] * normal[2]
    trans_mat[0, 2] = -2. * normal[0] * normal[2]
    trans_mat[1, 2] = -2. * normal[1] * normal[2]
    trans_mat[2, 2] = 1. - 2. * normal[2] ** 2.

    # Apply operations
    coords = coords @ trans_mat

    return coords


def find_entities(labels, coords, adjust_cutoff={}, non_bond_labels=[]):
    '''
    Finds formulae of entities given in labels and coords using adjacency
    matrix

    Parameters
    ----------
    labels: list[str]
        atomic labels
    coords: np.ndarray
        xyz coordinates of each atom as (n_atoms, 3) array
    adjust_cutoff: dict, optional
        dictionary of atoms (keys) and new cutoffs (values) used in generating
        adjacency matrix
    non_bond_labels: list, optional
        List of atomic labels specifying atoms to which no bonds will be
        allowed.\n
        e.g If a metal centre is provided this will result in single ligands\n
        being returned.

    Returns
    -------
    dict[str:list[list[int]]]
        keys = molecular formula\n
        vals = list of lists, where each list contains the indices of a single
        \noccurrence of the `key`, and the indices match the order given\n
        in `labels` and `coords`
    '''

    # Remove label numbers if present
    labels_nn = remove_label_indices(labels)

    # Generate adjacency matrix using ASE
    adjacency = get_adjacency(labels_nn, coords, adjust_cutoff=adjust_cutoff)

    no_bond_indices = [
        it for it, lab in enumerate(labels)
        if lab in non_bond_labels
    ]

    if not len(no_bond_indices):
        print('Cannot find specified no_bond atoms, perhaps try with index included?')

    for nbi in no_bond_indices:
        adjacency[nbi, :] = 0
        adjacency[:, nbi] = 0

    # Find entities
    entities = find_entities_from_adjacency(labels_nn, adjacency)

    return entities


def find_entities_from_adjacency(labels_nn, adjacency):
    '''
    Finds formulae of entities given in labels and adjacency matrix

    Parameters
    ----------
    labels: list[str]
        atomic labels
    adjacency: np.ndarray
        Adjacency matrix (0,1) with same order as labels

    Returns
    -------
    dict[str:list[list[int]]]
        keys = molecular formula\n
        vals = list of lists, where each list contains the indices of a single
        \noccurrence of the `key`, and the indices match the order given\n
        in `labels` and `coords`
    '''

    # Count number of atoms
    n_atoms = len(labels_nn)

    # Set current fragment as start atom
    curr_frag = {0}

    # List of unvisited atoms
    unvisited = set(np.arange(n_atoms))

    # Dictionary of molecular_formula:[[indices_mol1], [indices_mol2]] pairs
    mol_indices = defaultdict(list)

    # Loop over adjacency matrix and trace out bonding network
    # Make a first pass, recording in a list the atoms which are bonded to the
    # first atom.
    # Then make another pass, and record in another list all the atoms bonded
    # to those in the previous list
    # and again, and again etc.
    while unvisited:
        # Keep copy of current fragment indices to check against for changes
        prev_frag = copy.copy(curr_frag)
        for index in prev_frag:
            # Find bonded atoms and add to current fragment
            indices = list(np.nonzero(adjacency[:, index])[0])
            curr_frag.update(indices)

        # If no changes in fragment last pass, then a complete structure must
        # have been found
        if prev_frag == curr_frag:

            # Generate molecular formula of current fragment
            curr_labels = [labels_nn[it] for it in curr_frag]
            curr_formula = count_elements(curr_labels)

            mol_indices[formdict_to_formstr(curr_formula)].append(
                list(curr_frag)
            )

            # Remove visited atoms
            unvisited = unvisited.difference(curr_frag)

            # Reset lists of labels and indices ready for next cycle
            curr_frag = {min(unvisited)} if unvisited else curr_frag

    mol_indices = dict(mol_indices)

    return mol_indices


def _calculate_rmsd(coords_1, coords_2):
    '''
    Calculates RMSD between two structures
    RMSD = sqrt(mean(deviations**2))
    Where deviations are defined as norm([x1,y1,z1]-[x2,y2,z2])

    Parameters
    ----------
    coords_1: np.ndarray
        xyz coordinates as (n_atoms, 3) array
    coords_2: np.ndarray
        xyz coordinates as (n_atoms, 3) array

    Returns
    -------
    float
        Root mean square of norms of deviation between two structures
    '''

    # Check there are the same number of coordinates
    assert len(coords_1) == len(coords_2)

    # Calculate difference between [x,y,z] of atom pairs
    diff = [trio_1 - trio_2 for trio_1, trio_2 in zip(coords_1, coords_2)]

    # Calculate square norm of difference
    norms_sq = [la.norm(trio)**2 for trio in diff]

    # Calculate mean of squared norms
    mean = np.mean(norms_sq)

    # Take square root of mean
    rmsd = np.sqrt(mean)

    return rmsd


def calculate_rmsd(coords_1, coords_2, mask_1=[], mask_2=[], order_1=[],
                   order_2=[]):
    '''
    Calculates RMSD between two structures\n
    RMSD = sqrt(mean(deviations**2))\n
    Where deviations are defined as norm([x1,y1,z1]-[x2,y2,z2])\n
    If coords_1 and coords_2 are not the same length, then a mask array can be
    \nprovided for either/both and is applied prior to the calculation\n
    coords_1 and coords_2 can also be reordered if new orders are specified
    - note this occurs BEFORE masking

    Parameters
    ----------
    coords_1: np.ndarray
        xyz coordinates as (n_atoms, 3) array
    coords_2: np.ndarray
        xyz coordinates as (n_atoms, 3) array

    mask_1: list
        list of 0 (exclude) and 1 (include) for each element in coords_1
    mask_2: list
        list of 0 (exclude) and 1 (include) for each element in coords_2
    order_1: list
        list of new indices for coords_1 - applied BEFORE masking
    order_2: list
        list of new indices for coords_2 - applied BEFORE masking

    Returns
    -------
    float
        Root mean square of norms of deviation between two structures
    '''

    # Set up new ordering
    if order_1:
        _order_1 = order_1
    else:
        _order_1 = range(len(coords_1))

    if order_2:
        _order_2 = order_2
    else:
        _order_2 = range(len(coords_2))

    # Apply new order
    _coords_1 = coords_1[_order_1]
    _coords_2 = coords_2[_order_2]

    # Set up masks
    if mask_1:
        _coords_1 = np.delete(_coords_1, mask_1, axis=0)

    # Set up masks
    if mask_2:
        _coords_2 = np.delete(_coords_2, mask_2, axis=0)

    # Calculate rmsd
    rmsd = _calculate_rmsd(_coords_1, _coords_2)

    return rmsd


def rotate_coords(coords, alpha, beta, gamma):
    '''
    Rotates coordinates by alpha, beta, gamma using the zyz convention
    https://easyspin.org/easyspin/documentation/eulerangles.html

    Parameters
    ----------
    coords: np.ndarray
        xyz coordinates as (n_atoms, 3) array
    alpha: float
        alpha angle in radians
    beta: float
        beta  angle in radians
    gamma: float
        gamma angle in radians

    Returns
    -------
    np.ndarray
        xyz coordinates as (n_atoms, 3) array after rotation
        in same order as input coordinates
    '''

    R = np.zeros([3, 3])

    # Build rotation matrix
    R[0, 0] = np.cos(gamma) * np.cos(beta) * np.cos(alpha) - np.sin(gamma) * np.sin(alpha) # noqa
    R[0, 1] = np.cos(gamma) * np.cos(beta) * np.sin(alpha) + np.sin(gamma) * np.cos(alpha) # noqa
    R[0, 2] = -np.cos(gamma) * np.sin(beta)
    R[1, 0] = -np.sin(gamma) * np.cos(beta) * np.cos(alpha) - np.cos(gamma) * np.sin(alpha) # noqa
    R[1, 1] = -np.sin(gamma) * np.cos(beta) * np.sin(alpha) + np.cos(gamma) * np.cos(alpha) # noqa
    R[1, 2] = np.sin(gamma) * np.sin(beta)
    R[2, 0] = np.sin(beta) * np.cos(alpha)
    R[2, 1] = np.sin(beta) * np.sin(alpha)
    R[2, 2] = np.cos(beta)

    # Create (n,3) matrix from coords list
    _coords = coords.T

    # Apply rotation matrix
    rot_coords = R @ _coords

    # Convert back to (3,n) matrix
    rot_coords = rot_coords.T

    return rot_coords


def minimise_rmsd(coords_1, coords_2, mask_1=[], mask_2=[], order_1=[],
                  order_2=[]):
    '''
    Minimises the RMSD between two structures
    by rotating coords_1 onto coords_2
    If coords_1 and coords_2 are not the same length, then a mask array can be
    provided for either/both and is applied prior to the calculation
    coords_1 and coords_2 can also be reordered if new orders are specified
    **note reordering occurs before masking**

    Parameters
    ----------
    coords_1: np.ndarray
        xyz coordinates as (n_atoms, 3) array
    coords_2: np.ndarray
        xyz coordinates as (n_atoms, 3) array
    mask_1: list[int]
        0 (exclude) or 1 (include) for each element in coords_1
    mask_2: list[int]
        0 (exclude) or 1 (include) for each element in coords_2
    order_1: list[int]
        new indices for coords_1 - applied BEFORE masking
    order_2: list[int]
        new indices for coords_2 - applied BEFORE masking

    Returns
    -------
    float
        Root mean square of norms of deviation between two structures
    float
        alpha angle in radians
    float
        beta angle in radians
    float
        gamma angle in radians
    '''

    # Set up new ordering
    if order_1:
        _order_1 = order_1
    else:
        _order_1 = range(len(coords_1))

    if order_2:
        _order_2 = order_2
    else:
        _order_2 = range(len(coords_2))

    # Apply new order
    _coords_1 = coords_1[_order_1]
    _coords_2 = coords_2[_order_2]

    # Set up masks
    if mask_1:
        _coords_1 = np.delete(_coords_1, mask_1, axis=0)

    # Set up masks
    if mask_2:
        _coords_2 = np.delete(_coords_2, mask_2, axis=0)

    # Fit alpha, beta, and gamma to minimise rmsd
    result = spo.least_squares(
        lambda angs: _rotate_and_rmsd(
            angs, _coords_1, _coords_2
        ),
        x0=(1., 1., 1.),
        jac='3-point'
    )

    # Get optimum angles
    [alpha, beta, gamma] = result.x
    rmsd = result.fun[0]

    return rmsd, alpha, beta, gamma


def _rotate_and_rmsd(angs, coords_1, coords_2):
    '''
    Rotates coords_1 by alpha, beta, gamma using the zyz convention
    https://easyspin.org/easyspin/documentation/eulerangles.html
    then calcualtes the rmsd between coords_1 and coords_2

    Parameters
    ----------
    coords_1: np.ndarray
        xyz coordinates as (n_atoms, 3) array of first system
    coords_2: np.ndarray
        xyz coordinates as (n_atoms, 3) array of second system
    angs: list[float]
        alpha, beta, gamma in radians

    Returns
    -------
    np.ndarray
        xyz coordinates as (n_atoms, 3) array after rotation
        in same order as input coordinates
    '''

    # Rotate coordinates of first system
    _coords_1 = rotate_coords(coords_1, angs[0], angs[1], angs[2])

    # Calculate rmsd between rotated first system and original second system
    rmsd = _calculate_rmsd(_coords_1, coords_2)

    return rmsd


def calculate_com(labels, coords):
    '''
    Calculates centre-of-mass using relative atomic masses

    Parameters
    ----------
    labels: list
        list of atomic labels
    coords: np.ndarray
        xyz coordinates as (n_atoms, 3) array

    Returns
    -------
    np.ndarray
        xyz coordinates of centre of mass as (3) array
    '''

    labels_nn = remove_label_indices(labels)

    masses = [atomic.masses[lab] for lab in labels_nn]

    com_coords = np.zeros(3)

    for trio, mass in zip(coords, masses):
        com_coords += trio * mass

    com_coords /= np.sum(masses)

    return com_coords
