#!/usr/local/opt/python@3.8/bin/python3.8
# -*- coding: utf-8 -*-

import click
import gaga
import gatetools.phsp as phsp
import torch
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import rc

rc('text', usetex=True)
rc('font', **{'family': 'DejaVu Sans', 'serif': ['Computer Modern']})


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('phsp1_filename')
@click.argument('phsp2_filename')
@click.argument('pth_filename')
@click.option('--n', '-n', default=1e6, help='Number of samples to generate')
@click.option('--nb_bins', '-b', default=int(351), help='Number of bins')




def gaga_plot(phsp1_filename, phsp2_filename, pth_filename, n, nb_bins):
    '''
    \b
    Plot marginal distributions from a GAN-PHSP

    \b
    <PHSP_FILENAME1>   : input phase space file PHSP file (.npy)
    <PHSP_FILENAME2>   : input GAN training phase space file PHSP (.npy)
    <PTH_FILENAME>    : input GAN PTH file (.pth)
    '''

    # nb of values
    n = int(n)
    radius = 350

    # load phsp
    real, r_keys, m = phsp.load(phsp1_filename, n)
    real2, r_keys2, m = phsp.load(phsp2_filename, n)


    # load pth
    params, G, D, optim, dtypef= gaga.load(pth_filename)
    f_keys = params['keys']
    keys = f_keys.copy()

    # generate samples
    fake = gaga.generate_samples2(params, G, n, -1, False, True)

    # Keep X,Y or convert to toggle


    #real, r_keys = phsp.add_missing_angle(real, r_keys, keys, radius)
    #real2, r_keys2 = phsp.add_missing_angle(real2, r_keys2, keys, radius)
    #fake, f_keys = phsp.add_missing_angle(fake, f_keys, keys, radius)


    real = phsp.select_keys(real, r_keys, keys)
    real2 = phsp.select_keys(real2, r_keys2, keys)
    fake = phsp.select_keys(fake, f_keys, keys)



    print("data sampled and generated")

    #histogram plots phsp vs gan
    keys = ['$E_{\mathrm{kin}}$ [MeV]', '$x$ [mm]', '$y$ [mm]', '$dx$', '$dy$', '$dz$']

    #plt.style.use('seaborn-paper')

    fig_row = 3
    fig_column = 2
    fig_size = (7, 7)

    z_multiplicator = 3

    nb_fig = len(keys)
    fig1, ax1 = plt.subplots(fig_row, fig_column, figsize= fig_size)

    indices_2by6 = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]
    #x_limits = [(0, 6.5), (-70, 70), (-70, 70), (-0.6, 0.6), (-0.6, 0.6), (0.88, 1.02)]
    x_limits = [(0, 6.5), (-80, 80), (-80, 80), (-0.6, 0.6), (-0.6, 0.6), (0.85, 1.02)]
    hist_range = [(0, 6.5), (-100, 100), (-100, 100), (-1, 1), (-1, 1), (0, 1)]

    i = 0
    data_real = np.zeros((nb_fig, n))
    data_fake = np.zeros((nb_fig, n))
    hist_real = np.zeros((nb_fig-1, nb_bins))
    bin_real = np.zeros((nb_fig-1, nb_bins+1))
    hist_fake = np.zeros((nb_fig-1, nb_bins))
    bin_fake = np.zeros((nb_fig-1, nb_bins+1))
    while i < nb_fig-1:
        for k in range(0, n):
            data_real[i][k] = real[k][i]
            data_fake[i][k] = fake[k][i]

        hist_real[i][:], bin_real[i][:] = np.histogram(data_real[i][:],
            bins = nb_bins, range= hist_range[i])
        hist_fake[i][:], bin_fake[i][:] = np.histogram(data_fake[i][:],
            bins = nb_bins, range= hist_range[i])

        ax1[indices_2by6[i]].hist(x= bin_real[i][:-1], weights= hist_real[i][:],
            bins= bin_real[i][:], alpha=0.4,
            align= 'mid', histtype= 'stepfilled', label='PHSP1')
        ax1[indices_2by6[i]].hist(x= bin_fake[i][:-1], weights= hist_fake[i][:],
            bins= bin_fake[i][:], alpha=0.4,
            align= 'mid', histtype= 'stepfilled', label=r'$G$')
        ax1[indices_2by6[i]].legend(loc=1, fancybox=True, edgecolor='black',
            frameon=True, markerscale=1.5)
        ax1[indices_2by6[i]].set(xlabel= (keys[i]), ylabel= ('Counts'))
        ax1[indices_2by6[i]].ticklabel_format(axis = 'y', style = 'sci',
            scilimits= (0,0))
        ax1[indices_2by6[i]].set_xlim(left= x_limits[i][0], right= x_limits[i][1])
        i += 1
    else:
        for k in range(0, n):
            data_real[i][k] = real[k][i]
            data_fake[i][k] = fake[k][i]
        hist_real_dz, bin_real_dz = np.histogram(data_real[i][:],
            bins = nb_bins*z_multiplicator, range= hist_range[i])
        hist_fake_dz, bin_fake_dz = np.histogram(data_fake[i][:],
            bins = nb_bins*z_multiplicator, range= hist_range[i])

        ax1[indices_2by6[i]].hist(x= bin_real_dz[:-1], weights= hist_real_dz[:],
            bins= bin_real_dz[:], alpha=0.4,
            align= 'mid', histtype= 'stepfilled', label='PHSP1')
        ax1[indices_2by6[i]].hist(x= bin_fake_dz[:-1], weights= hist_fake_dz[:],
            bins= bin_fake_dz[:], alpha=0.4,
            align= 'mid', histtype= 'stepfilled', label=r'$G$')
        ax1[indices_2by6[i]].legend(loc=2, fancybox=True, edgecolor='black',
            frameon=True, markerscale=1.5)
        ax1[indices_2by6[i]].set(xlabel= (keys[i]), ylabel= ('Counts'))
        ax1[indices_2by6[i]].ticklabel_format(axis = 'y', style = 'sci',
            scilimits= (0,0))
        ax1[indices_2by6[i]].set_xlim(left= x_limits[i][0], right= x_limits[i][1])



    plt.tight_layout(w_pad=0.5, h_pad=0.5)


    # histogram phsp vs phsp

    i = 0
    fig3, ax3 = plt.subplots(fig_row, fig_column, figsize=fig_size)

    data_real2 = np.zeros((nb_fig, n))
    hist_real2 = np.zeros((nb_fig-1, nb_bins))
    bin_real2 = np.zeros((nb_fig-1, nb_bins+1))

    while i < nb_fig-1:
        for k in range(0, n):
            data_real2[i][k] = real2[k][i]

        hist_real2[i][:], bin_real2[i][:] = np.histogram(data_real2[i][:],
            bins = nb_bins, range= hist_range[i])

        ax3[indices_2by6[i]].hist(x= bin_real[i][:-1], weights= hist_real[i][:],
            bins= bin_real[i][:], alpha=0.4,
            align= 'mid', histtype= 'stepfilled', label='PHSP1')
        ax3[indices_2by6[i]].hist(x= bin_real2[i][:-1], weights= hist_real2[i][:],
            bins= bin_real2[i][:], alpha=0.4,
            align= 'mid', histtype= 'stepfilled', label='PHSP2')
        ax3[indices_2by6[i]].legend(loc=1, fancybox=True, edgecolor='black',
            frameon=True, markerscale=1.5)
        ax3[indices_2by6[i]].set(xlabel= (keys[i]), ylabel= ('Counts'))
        ax3[indices_2by6[i]].ticklabel_format(axis = 'y', style = 'sci',
            scilimits= (0,0))
        ax3[indices_2by6[i]].set_xlim(left= x_limits[i][0], right= x_limits[i][1])
        i += 1
    else:
        for k in range(0, n):
            data_real2[i][k] = real2[k][i]
        hist_real2_dz, bin_real2_dz = np.histogram(data_real2[i][:],
            bins = nb_bins*z_multiplicator, range= hist_range[i])

        ax3[indices_2by6[i]].hist(x= bin_real_dz[:-1], weights= hist_real_dz[:],
            bins= bin_real_dz[:], alpha=0.4,
            align= 'mid', histtype= 'stepfilled', label='PHSP1')
        ax3[indices_2by6[i]].hist(x= bin_real2_dz[:-1], weights= hist_real2_dz[:],
            bins= bin_real2_dz[:], alpha=0.4,
            align= 'mid', histtype= 'stepfilled', label='PHSP2')
        ax3[indices_2by6[i]].legend(loc=2, fancybox=True, edgecolor='black',
            frameon=True, markerscale=1.5)
        ax3[indices_2by6[i]].set(xlabel= (keys[i]), ylabel= ('Counts'))
        ax3[indices_2by6[i]].ticklabel_format(axis = 'y', style = 'sci',
            scilimits= (0,0))
        ax3[indices_2by6[i]].set_xlim(left= x_limits[i][0], right= x_limits[i][1])

    plt.tight_layout(w_pad=0.5, h_pad=0.5)

    # differences of histograms

    keys_diff = ['$E_{\mathrm{kin}}$ difference [\%]', '$x$ difference [\%]',
        '$y$ difference [\%]', '$dx$ difference [\%]', '$dy$ difference [\%]',
        '$dz$ difference [\%]']
    x_limits_diff = [(-20, 20), (-20, 20), (-20, 20), (-20, 20), (-20, 20), (-30, 30)]
    y_limits_diff = [(0, 120)]


    hist_real_adjust = hist_real
    hist_real_dz_adjust = hist_real_dz

    for row in range(0, nb_fig-1):
        for column in range (0, nb_bins):
            if hist_real_adjust[row][column] == 0:
                hist_real_adjust[row][column] = 10

    for column in range (0, nb_bins * z_multiplicator):
        if hist_real_dz_adjust[column] == 0:
            hist_real_dz_adjust[column] = 10

    differences = (hist_fake - hist_real)/hist_real_adjust * 100
    differences_dz = (hist_fake_dz - hist_real_dz)/hist_real_dz_adjust * 100
    nb_bins_diff = 131

    fig2, ax2 = plt.subplots(fig_row, fig_column, figsize=fig_size)
    i = 0
    while i < nb_fig-1:
        ax2[indices_2by6[i]].hist(differences[i][:], bins= nb_bins_diff, alpha=0.4, color= 'g',
            align= 'mid', histtype= 'stepfilled', range = (-40,40), label=r'PHSP1 vs. $G$')
        #ax2[indices_2by6[i]].vlines(np.mean(differences[i][:]), ymin=y_limits_diff[0][0],
        #    ymax=y_limits_diff[0][1], colors='g', linestyles='dashed', linewidth=0.6, label = r'mean $G$')
        i += 1
    else:
        ax2[indices_2by6[i]].hist(differences_dz, bins= nb_bins_diff, alpha=0.4, color= 'g',
            align= 'mid', histtype= 'stepfilled', range = (-40,40), label=r'PHSP1 vs. $G$')
        #ax2[indices_2by6[i]].vlines(np.mean(differences_dz), ymin=y_limits_diff[0][0],
        #    ymax=y_limits_diff[0][1], colors='g', linestyles='dashed', linewidth=0.6, label = r'mean $G$')


    hist_real2_adjust = hist_real2
    hist_real2_dz_adjust = hist_real2_dz

    for row in range(0, nb_fig-1):
        for column in range (0, nb_bins):
            if hist_real2_adjust[row][column] == 0:
                hist_real2_adjust[row][column] = 10

    for column in range (0, nb_bins * z_multiplicator):
        if hist_real2_dz_adjust[column] == 0:
            hist_real2_dz_adjust[column] = 10

    differences2 = (hist_real2 - hist_real)/hist_real_adjust * 100
    differences2_dz = (hist_real2_dz - hist_real_dz)/hist_real_dz_adjust * 100

    i = 0
    while i < nb_fig-1:
        ax2[indices_2by6[i]].hist(differences2[i][:], bins= nb_bins_diff, alpha=0.4, color= 'm',
            align= 'mid', histtype= 'stepfilled', range = (-40,40), label='PHSP1 vs. PHSP2')
        #ax2[indices_2by6[i]].vlines(np.mean(differences2[i][:]), ymin=y_limits_diff[0][0],
        #    ymax=y_limits_diff[0][1], colors='r', linestyles='dashed', linewidth=0.6, label = 'mean PHSP')
        ax2[indices_2by6[i]].legend(loc=2, fancybox=True, edgecolor='black',
            frameon=True, markerscale=1.5)
        ax2[indices_2by6[i]].set(xlabel= (keys_diff[i]), ylabel= ('Counts'))
        ax2[indices_2by6[i]].set_ylim(y_limits_diff[0])
        ax2[indices_2by6[i]].set_xlim(x_limits_diff[i])
        ax2[indices_2by6[i]].ticklabel_format(axis = 'y', style = 'sci',
            scilimits= (0,0))
        #ax1_twin = ax1[indices_2by6[i]].twinx()
        #ax1_twin.plot(bin_real2[i][20:-21], differences[i][20:-20])

        i += 1
    else:
        ax2[indices_2by6[i]].hist(differences2_dz, bins= nb_bins_diff, alpha=0.4, color= 'm',
            align= 'mid', histtype= 'stepfilled', range = (-40,40), label='PHSP1 vs. PHSP2')
        #ax2[indices_2by6[i]].vlines(np.mean(differences2_dz), ymin=y_limits_diff[0][0],
        #    ymax=y_limits_diff[0][1], colors='r', linestyles='dashed', linewidth=0.6, label = 'mean PHSP')
        ax2[indices_2by6[i]].legend(loc=2, fancybox=True, edgecolor='black',
            frameon=True, markerscale=1.5)
        ax2[indices_2by6[i]].set(xlabel= (keys_diff[i]), ylabel= ('Counts'))
        ax2[indices_2by6[i]].set_ylim(y_limits_diff[0])
        ax2[indices_2by6[i]].set_xlim(x_limits_diff[i])
        ax2[indices_2by6[i]].ticklabel_format(axis = 'y', style = 'sci',
            scilimits= (0,0))

    plt.tight_layout(w_pad=0.5, h_pad=0.5)





    # remove empty plot
    #phsp.fig_rm_empty_plot(nb_fig, ax)
    #plt.close()
    plt.show()
    #plt.savefig(str(plot_filename))

# --------------------------------------------------------------------------
# phsp = 'data/TrueBeam_v2_6X_03.npy'
# pth = 'pth/003.pth'
# nb_primary = 1e5
# nb_bin = 30


if __name__ == '__main__':
    gaga_plot()
