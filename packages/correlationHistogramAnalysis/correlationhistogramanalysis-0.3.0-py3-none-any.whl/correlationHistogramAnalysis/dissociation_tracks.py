"""
Created on Fri Oct 20 06:59:38 2023

@author: Katnagallu
"""
from itertools import permutations, product
import numpy as np
from collections import Counter


def parse_formula(formula):
    """Works for formulas of form AxBy where x,y=1 do not have to be mentioned otherwise x,y <=9"""
    elements = {}
    for char, nxtchar, nxt2char in zip(
        formula, formula[1:] + formula[:1], formula[2:] + formula[:2]
    ):
        if char.isalpha() & char.isupper():
            if nxtchar.isalpha() & nxtchar.islower():
                if nxt2char.isnumeric():
                    elements[char + nxtchar] = int(nxt2char)
                elif nxt2char.isalpha():
                    elements[char + nxtchar] = int(1)
            elif nxtchar.isupper():
                elements[char] = int(1)
            elif nxtchar.isnumeric:
                elements[char] = int(nxtchar)
            else:
                elements[char] = int(nxtchar)
    prime_list = [2, 3, 5, 7, 9, 11, 13, 17, 19, 23, 31, 37, 41, 43, 47]
    elements_prime = dict(
        [(y, prime_list[x]) for x, y in enumerate(sorted(set(elements)))]
    )
    return elements, elements_prime


def generate_pair_products(elements):
    pairs = set()
    for permutation in permutations(elements):
        for i in range(1, len(permutation)):
            first_product = permutation[:i]
            second_product = permutation[i:]
            pair = (first_product, second_product)
            reverse_pair = (second_product, first_product)
            if pair not in pairs and reverse_pair not in pairs:
                pairs.add(pair)
    return pairs


def charge_shuffler(charge, num_products):
    charges_p = list()
    for p in product(range(charge + 1), repeat=num_products):
        if sum(p) == charge:
            charges_p.append(p)
    return charges_p


def generate_triple_products(elements):
    triplets = set()
    for permutation in permutations(elements):
        for i in range(1, len(permutation)):
            first_product = permutation[:i]
            temp = permutation[i:]
            for j in range(1, len(temp)):
                second_product = temp[:j]
                third_product = temp[j:]
                trip = (
                    tuple(sorted(first_product)),
                    tuple(sorted(second_product)),
                    tuple(sorted(third_product)),
                )
                triplet = tuple(sorted(trip))  # Sort the elements to ensure uniqueness
                if triplet not in triplets:
                    triplets.add(triplet)
    return triplets


def product_reparser(p1):
    product = []
    for key, value in p1.items():
        if value == 0:
            continue
        if value == 1:
            product.append(key)
        else:
            product.append(key + str(p1[key]))

    product = "".join(product)
    return product


def possible_product_pairs(complex_formula, charge):
    """Based on the chemical formula, product pairs are generated efficiently."""
    original_dict, _ = parse_formula(complex_formula)

    def szudzik_pairing(a, b):
        """returns a unique number for a pair of integer, which is insensitive to order in pairs"""
        return a * a + b if a >= b else a + b * b

    def generate_pairs(parsed_dict):
        keys = list(parsed_dict.keys())
        values = list(parsed_dict.values())

        def generate_recursive_pairs(current_pair, remaining_values, remaining_keys):
            if not remaining_keys:
                return [current_pair]

            key = remaining_keys[0]
            value = remaining_values[0]
            remaining_values = remaining_values[1:]
            remaining_keys = remaining_keys[1:]

            pairs = []
            for i in range(value + 1):
                pair1 = {key: i}
                pair2 = {key: value - i}
                new_pair = {**current_pair, **pair1}
                pairs.extend(
                    generate_recursive_pairs(new_pair, remaining_values, remaining_keys)
                )
                new_pair = {**current_pair, **pair2}
                pairs.extend(
                    generate_recursive_pairs(new_pair, remaining_values, remaining_keys)
                )

            return pairs

        all_pairs = generate_recursive_pairs({}, values, keys)
        unique_permutations = [
            dict(y) for y in set(tuple(x.items()) for x in all_pairs)
        ]
        return unique_permutations

    unique_perms = generate_pairs(original_dict)
    daughter_1 = {}
    daughter_2 = {}
    count = 0
    prime_list = [2, 3, 5, 7, 9, 11, 13, 17, 19, 23, 31, 37, 41, 43, 47]
    elements_prime = dict(
        [
            (y, prime_list[x])
            for x, y in enumerate(sorted(set(list(original_dict.keys()))))
        ]
    )

    for i in range(len(unique_perms)):
        if (
            all(value == 0 for value in unique_perms[i].values())
            or unique_perms[i] == original_dict
        ):
            continue
        daughter_1[count] = unique_perms[i]
        daughter_2[count] = {
            key: original_dict[key] - unique_perms[i][key]
            for key in original_dict.keys()
        }
        count += 1

    sp = []
    for i in range(len(daughter_1)):
        k = [elements_prime[key] ** daughter_1[i][key] for key in daughter_1[i].keys()]
        l = [elements_prime[key] ** daughter_2[i][key] for key in daughter_2[i].keys()]
        sp.append(szudzik_pairing(np.product(k), np.product(l)))
    _, inds = np.unique(sp, return_index=True)
    prod1 = {nk: daughter_1[key] for key, nk in zip(inds, range(len(inds)))}
    prod2 = {nk: daughter_2[key] for key, nk in zip(inds, range(len(inds)))}
    ccp = charge_shuffler(charge, num_products=2)

    return prod1, prod2, ccp


def possible_product_triplets(complex_formula, charge):
    ss, ssp = parse_formula(complex_formula)
    repeated_elements = list(Counter(ss).elements())
    elements = []
    for e in repeated_elements:
        elements.append(ssp[e])
    triplets = generate_triple_products(elements)
    prod_triplets = []
    for r in sorted(triplets):
        prod_triplets.append(np.prod(r[0]))
    ss = sorted(triplets)
    a, r = np.unique(prod_triplets, return_index=True)
    products = [ss[r[i]] for i in range(len(r))]
    product_trip_1 = dict()
    product_trip_2 = dict()
    product_trip_3 = dict()
    for count, i in enumerate(products):
        m, c = np.unique(i[0], return_counts=True)
        prod_1 = dict()
        for k in range(len(m)):
            for key, value in ssp.items():
                if value == m[k]:
                    prod_1[key] = c[k]
        product_trip_1[count] = prod_1
        m, c = np.unique(i[1], return_counts=True)
        prod_2 = dict()
        for k in range(len(m)):
            for key, value in ssp.items():
                if value == m[k]:
                    prod_2[key] = c[k]
        product_trip_2[count] = prod_2
        m, c = np.unique(i[2], return_counts=True)
        prod_3 = dict()
        for k in range(len(m)):
            for key, value in ssp.items():
                if value == m[k]:
                    prod_3[key] = c[k]
        product_trip_3[count] = prod_3
    ccp = charge_shuffler(charge, num_products=3)

    return product_trip_1, product_trip_2, product_trip_3, ccp


def associate_mass(
    elements_mass,
    complex_formula=None,
    parent_charge=None,
    product_1=None,
    product_2=None,
    charge_states=None,
    react_dict=None,
):
    if react_dict is not None:
        complex_formula = react_dict["parent"]
        parent_charge = react_dict["cp"]
        product_1, _ = parse_formula(react_dict["daughter_1"])
        product_2, _ = parse_formula(react_dict["daughter_2"])
        charge_states = [react_dict["cd1"], react_dict["cd2"]]
    mp = 0
    ss, _ = parse_formula(complex_formula)
    for key, value in ss.items():
        mp += elements_mass[key] * value / parent_charge
    md1 = 0
    md2 = 0
    for key, value in product_1.items():
        try:
            md1 += elements_mass[key] * value / charge_states[0]
        except ZeroDivisionError:
            md1 = 1e10
    for key, value in product_2.items():
        try:
            md2 += elements_mass[key] * value / charge_states[1]
        except ZeroDivisionError:
            md2 = 1e10
    return mp, md1, md2


def digitize_track(m1e, m2e, m1d, m2d, h):
    track_count = h[np.digitize(m1d, m2e) - 2, np.digitize(m2d, m1e) - 2][::-1]
    return track_count


def index_values_in_bin(m1, m2, ind, m1e, m2e, bins_along_track):
    indices_in_bin = []
    for i in range(len(bins_along_track)):
        indices_m1 = np.where(
            (m1[ind] >= m1e[bins_along_track[i, 0]])
            & (m1[ind] < m1e[bins_along_track[i, 0] + 1])
        )[0]
        indices_m2 = np.where(
            (m2[ind] >= m2e[bins_along_track[i, 1]])
            & (m2[ind] < m2e[bins_along_track[i, 1] + 1])
        )[0]
        if len(np.intersect1d(indices_m1, indices_m2)) != 0:
            indices_in_bin.append(np.intersect1d(indices_m1, indices_m2))
    indices_in_bin = np.concatenate(indices_in_bin)
    return indices_in_bin
