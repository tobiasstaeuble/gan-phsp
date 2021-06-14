#!/usr/local/opt/python@3.8/bin/python3.8
# -*- coding: utf-8 -*-

import click
import numpy as np
import gaga
import torch
from shutil import copyfile
from matplotlib import pyplot as plt
from matplotlib import rc

rc('text', usetex=True)
rc('font', **{'family': 'DejaVu Sans', 'serif': ['Computer Modern']})


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('pth_filename', nargs=-1)
@click.option('--plot/--no-plot', default=True)
@click.option('--add_energy', default=float(-1),
              help='Add the key Ekine with the given value in the parameters of the pth file')
def gaga_info(pth_filename, plot, add_energy):
    '''
    \b
    Print information about a trained GAN phase space.
    If --plot option: plot the loss wrt epoch

    \b
    <PTH_FILENAME> : input PTH file (.pth)
    '''


    # ----------------------------------------------------------------------------
    def number_spliter(array_old, each_sample):
        length_old = len(array_old) - 1
        length = int(length_old/each_sample)
        array_x = np.arange(0, length_old, each_sample)
        array_y = np.zeros(length)
        for i in range(0,length):
            array_y[i] = array_old[i*each_sample]
        return array_x, array_y




    def plot_epoch(ax, optim, filename):
        '''
        Plot D loss wrt to epoch
        3 panels : all epoch / first 20% / last 1%
        '''

        #x1 = np.asarray(optim['d_loss_real'])
        #x2 = np.asarray(optim['d_loss_fake'])
        #y1 = np.asarray(optim['g_loss_real'])
        #y2 = np.asarray(optim['g_loss_fake'])
        x = np.asarray(optim['d_loss'])
        y = -np.asarray(optim['g_loss'])

        x_d, y_nx = number_spliter(x, 500)
        y_d, y_ny = number_spliter(y, 500)

        a = ax[0]
        l = filename
        a.plot(x_d, y_nx, '-', label='$J_D$')
        a.plot(y_d, y_ny, '-', label='$J_G$')
        z = np.zeros_like(x)
        a.set_xlabel('Iteration')
        a.set_ylabel('Loss')
        a.set_ylim(-0.015,0.0215)
        a.plot(z, '--')
        a.legend()


        a = ax[1]
        n = int(len(x)*0.05) # first 20%
        xc = x[0:n+1]
        yc = y[0:n+1]
        x_d_zoom, y_nx_zoom = number_spliter(xc, 20)
        y_d_zoom, y_ny_zoom = number_spliter(yc, 20)

        a.plot(x_d_zoom, y_nx_zoom, '-', label='$J_D$')
        a.plot(y_d_zoom, y_ny_zoom, '-', label='$J_G$')
        z = np.zeros_like(xc)
        a.set_xlabel('Iteration')
        a.set_ylabel('Loss')
        a.set_xlim((0,n))
        a.set_ylim((-0.015,0.005))
        a.plot(z, 'g--')
        a.legend()

    # ----------------------------------------------------------------------------


    if plot:
        fig, ax = plt.subplots(2, 1, figsize=(6,5))

    for f in pth_filename:
        params, G, D, optim, dtypef = gaga.load(f)
        #gaga.print_info(params, optim)
        if plot:
            plot_epoch(ax, optim, f)
            #gaga.plot_epoch_wasserstein(ax, optim, f)

    if plot:
        plt.tight_layout()
        #plt.savefig('a.pdf', dpi=fig.dpi)
        plt.show()


# --------------------------------------------------------------------------
if __name__ == '__main__':
    gaga_info()
