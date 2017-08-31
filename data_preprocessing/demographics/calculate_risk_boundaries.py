"""
Determines high and low risk boundaries for different demographic factors
"""

import pandas as pd
import numpy as np

age_ed = pd.read_csv('ed_subset/mf_age_ed.csv')
age_irl = pd.read_csv('ed_subset/mf_age_irl.csv')
fam_ed = pd.read_csv('ed_subset/fam_stat_ed.csv')
df_fam_ed = fam_ed.ix[:, 10:]
fam_irl = pd.read_csv('ed_subset/fam_stat_irl.csv').ix[:, 10:]
ind_ed = pd.read_csv('ed_subset/ind_stat_ed.csv')
ind_irl = pd.read_csv('ed_subset/ind_stat_irl.csv')

job_ed = pd.read_csv('ed_subset/job_stat_ed.csv')
job_irl = pd.read_csv('ed_subset/job_stat_irl.csv').ix[:, 3:]

prince_ed = pd.read_csv('ed_subset/prince_stat_ed.csv')
prince_irl = pd.read_csv('ed_subset/prince_stat_irl.csv').ix[:, 4:]

house_ed = pd.read_csv('ed_subset/house_stat_ed.csv').ix[:, 4:]
house_irl = pd.read_csv('ed_subset/house_stat_irl.csv').ix[:, 4:]


mort_ed = house_ed.ix[:, 17:25]
mort_irl = house_irl.ix[:, 17:25]

mort_irl = mort_irl/(mort_irl['occu_total_hh'][0])


morts = []

for i in mort_ed.index:
    id = mort_ed.iloc[i, 1]

    ed_mort = mort_ed.iloc[i, :]/(mort_ed.iloc[i, :]['occu_total_hh'])

    morts.append(ed_mort['oo_wm'])

print(np.mean(morts))
print(np.std(morts))
print(len([i for i in morts if i > (0.32 + 1.22 * 0.09666)]))


occu_ed = house_ed.ix[:, -4:]
occu_irl = house_irl.ix[:, -4:]

occu_irl = occu_irl/(occu_irl.values.sum())

occus = []

for i in occu_ed.index:
    id = occu_ed.iloc[i, 1]

    ed_occu = occu_ed.iloc[i, :]/(occu_ed.iloc[i, :].values.sum())

    occus.append(ed_occu['occupied'])

print(np.mean(occus))
print(np.std(occus))
print(len([i for i in occus if i < (0.824311 - 1.3 * 0.1077)]))

prince_irl = prince_irl / (prince_irl['stat_total'].values.sum())

princes = []

for i in job_ed.index:
    id = job_ed.iloc[i, 1]

    ed_prince = prince_ed.iloc[i, 4:-1]/prince_ed.iloc[i, :]['stat_total']

    # jobs.append((max(ed_job), id))
    princes.append(ed_prince['work'])

print(np.mean(princes))
print(np.std(princes))
# print(sorted(princes))
# print(sorted(princes, reverse=True))

for j in range(1, 4):
    print(">" + str(1 + 0.1 * j) + " std above mean: ",
          len([i for i in princes if i > np.mean(princes) + np.std(princes)
               * (1 + 0.1 * j)]))
for j in range(1, 4):
    print(">" + str(1 + 0.1 * j) + " std below mean: ",
          len([i for i in princes if i < np.mean(princes) + np.std(princes)
               * -(1 + 0.1 * j)]))

job_irl = job_irl/(job_irl['class_total'].values.sum())
jobs = []

for i in job_ed.index:
    id = job_ed.iloc[i, 1]

    ed_job = job_ed.iloc[i, 4:-1]/job_ed.iloc[i, :]['class_total']

    # jobs.append((max(ed_job), id))
    jobs.append(max(ed_job))

print(np.mean(jobs))
print(np.std(jobs))
# print(sorted(jobs))
# print(sorted(jobs, reverse=True))
for j in range(1, 4):
    print(">" + str(j) + " std above mean: ",
          len([i for i in jobs if i > np.mean(jobs) + np.std(jobs) * j]))
for j in range(1, 4):
    print(">" + str(j) + " std below mean: ",
          len([i for i in jobs if i < np.mean(jobs) + np.std(jobs) * -j]))
print(len([i for i in jobs if i > 0.38]))
print(len([i for i in jobs if i < 0.23]))

inds = []
for i in ind_ed.index:
    ed_ind = ind_ed.iloc[i, 4:-1]/ind_ed.iloc[i, :]['ind_total']
    # print(max(ed_ind.index))
    # inds.append((max(ed_ind), ed_ind.idxmax()))
    inds.append(max(ed_ind))

# print(sorted(inds))
# print(sorted(inds, reverse=True))
print(len([i for i in inds if i > 0.32]))
print(len([i for i in inds if i < 0.215]))


fam_irl = fam_irl/(fam_irl['fam_total'].values.sum())
natave_enest = fam_irl['empty_nest'][0]
natave_ret = fam_irl['retired'][0]

enest_dif = []
ret_dif = []

for i in df_fam_ed.index:
    id = fam_ed.iloc[i, 1]

    ed_fam = df_fam_ed.iloc[i, :]/df_fam_ed.iloc[i, :]['fam_total']
    ed_enest = ed_fam['empty_nest']
    ed_ret = ed_fam['retired']

    enest_dif.append(ed_enest - natave_enest)
    ret_dif.append(ed_ret - natave_ret)

    # enest_dif.append((ed_enest - natave_enest, id))
    # ret_dif.append((ed_ret - natave_ret, id))

print(natave_enest * 100)
# print(sorted(enest_dif)) # 'E08068' Ridge, The Ridge, County Carlow
# print(sorted(enest_dif, reverse=True)) # 'E27030' Errislannan, R341,
# Shannanagower, Co. Galway
# print(sorted(ret_dif)) # 'E07067'
# print(sorted(ret_dif, reverse=True)) # 'E03049' Terenure-St. James

# If either is high risk, that takes precedence:
# 'E07063' Ballyvool Grove Farm House, Ballycocksoost, Inistioge, Co. Kilkenny

print(enest_dif)
print(np.mean(enest_dif))  # 0.00721658411136
print(np.std(enest_dif))  # 0.0246904980043
print(max(enest_dif))  # 0.136886985684
print(min(enest_dif))  # -0.0631130143165
for j in range(1, 4):
    print(">" + str(j) + " std above mean: ",
          len([i for i in enest_dif if i > np.std(enest_dif) * 1.6]))
for j in range(1, 4):
    print(">" + str(j) + " std below mean: ",
          len([i for i in enest_dif if i < np.std(enest_dif) * -0.85]))
# >1 std above mean:  709
# >2 std above mean:  188
# >3 std above mean:  52
# >1 std below mean:  224
# >2 std below mean:  8
# >3 std below mean:  0

print('\n')
print(ret_dif)
print(np.mean(ret_dif))  # 0.00414485529396
print(np.std(ret_dif))  # 0.0263978862721
print(max(ret_dif))  # 0.23268079554
print(min(ret_dif))  # -0.0499474672864
for j in range(1, 4):
    print(">" + str(j) + " std aboce mean: ", len([i for i in ret_dif if
                                                   i > np.std(ret_dif) * j]))
for j in range(1, 4):
    print(">" + str(j) + " std below mean: ", len([i for i in ret_dif if
                                                   i < np.std(ret_dif) * -j]))

# >1 std above mean:  511
# >2 std above mean:  158
# >3 std above mean:  62
# >1 std below mean:  256
# >2 std below mean:  0
# >3 std below mean:  0

# Age Info:
df_irl_m = age_irl.ix[:, range(4, 22, 1)]
df_irl_f = age_irl.ix[:, range(22, 40, 1)]

pop_m = df_irl_m.values.sum()
pop_f = df_irl_f.values.sum()

df_irl_m = df_irl_m/pop_m
df_irl_f = df_irl_f/pop_f

aucs = []
ids = []

for i in age_ed.index:
    id = age_ed.iloc[i, 1]

    ed_m = age_ed.iloc[i, 4:22]
    ed_f = age_ed.iloc[i, 22:40]

    ed_pop_m = ed_m.values.sum()
    ed_pop_f = ed_f.values.sum()

    ed_m = ed_m / ed_pop_m
    ed_f = ed_f / ed_pop_f

    auc = 0

    # Old Method: (High score means low risk)
    # for j in ed_m.index:
    #     a = j.split('_')[1]
    #     if len(a) == 3:
    #         ma = 90
    #     elif len(a) == 2:
    #         ma = 0
    #     elif int(a[:2]) >= 50:
    #         ma = np.mean([int(a[:2]), int(a[2:])]) + 0.5
    #     else:
    #         ma = 0
    #
    #     m_na = df_irl_m.loc[:, j][0] * 100
    #     m = ed_m.loc[j] * 100
    #     if m_na > m:
    #         auc += (m_na - m) * ma
    #
    # for j in ed_f.index:
    #     a = j.split('_')[1]
    #     if len(a) == 3:
    #         ma = 90
    #     elif len(a) == 2:
    #         ma = 0
    #     elif int(a[:2]) >= 50:
    #         ma = np.mean([int(a[:2]), int(a[2:])]) + 0.5
    #     else:
    #         ma = 0
    #
    #     f_na = df_irl_f.loc[:, j][0] * 100
    #     f = ed_f.loc[j] * 100
    #     if f_na > f:
    #         auc += (f_na - f) * ma

    # New Method: (High score means high risk)
    for j in ed_m.index:
        a = j.split('_')[1]
        if len(a) == 3:
            ma = 90
        elif len(a) == 2:
            ma = 0
        elif int(a[:2]) >= 50:
            ma = np.mean([int(a[:2]), int(a[2:])]) + 0.5
        else:
            ma = 0

        m_na = df_irl_m.loc[:, j][0] * 100
        m = ed_m.loc[j] * 100
        if m > m_na:
            auc += (m - m_na) * ma

    for j in ed_f.index:
        a = j.split('_')[1]
        if len(a) == 3:
            ma = 90
        elif len(a) == 2:
            ma = 0
        elif int(a[:2]) >= 50:
            ma = np.mean([int(a[:2]), int(a[2:])]) + 0.5
        else:
            ma = 0

        f_na = df_irl_f.loc[:, j][0] * 100
        f = ed_f.loc[j] * 100
        if f > f_na:
            auc += (f - f_na) * ma

    # aucs.append((auc, id))
    aucs.append(auc)

# print(sorted(aucs))
# print(sorted(aucs, reverse=True))
print(np.mean(aucs))
print(np.std(aucs))

print(len([i for i in aucs if i > 1000 + 406 * 1.25]))

# print(sorted(aucs))
# print(sorted(aucs, reverse=True))

# Old:
# Best: Derryfadda Road, Cappavilla 'E16107' (highest score)
# Worst: Claremont Park, Sandymount 'E02126' (lowest score)

# New:
# Best: Vinegar Hill Lane 'E14021' (lowest score)
# Worst: Coomacullen, Co. Cork 'E18045' (highest-ish score)

print(np.mean(aucs))
# Old: 991.134696699
# New: 1309.92332309
print(np.std(aucs))
# Old: 401.801786361
# New: 654.697361176
print(np.min(aucs))
# Old: 201
# New: 156
print(np.max(aucs))
# Old: 4084
# New: 4806
print(len(aucs))
# 3409

# Old:
# mean: 438, sd: 370
print(len(aucs))
print(len([i for i in aucs if i > 952 + 1.4*706.2]))
# >3 std above mean: 43
# >2 std above mean: 134
# >1 std above mean: 437
print(len([i for i in aucs if i < 991 - 401]))
# >1 std below mean: 405

print(len([i for i in aucs if i > 1309 + 654]))
# >3 std above mean: 37
# >2 std above mean: 154
# >1 std above mean: 513
print(len([i for i in aucs if i < 1309 - 654]))
# >1 std below mean: 490
