#!/usr/bin/env python
'''
This script reports the yearly SCG compute cost for a lab account and plots the per-month cost
Author: Aziz Khan <azizk@stanford.edu>
Date: March 25, 2024
'''
import os
import click
import matplotlib.pyplot as plt
import pandas as pd
import subprocess

@click.command()
@click.option('-a', '--account', required=True, help='PI SUNet ID')
@click.option('-y', '--year', required=True, type=int, help='Year')
@click.option('-p', '--plot', is_flag=True, default=False, help='Plot the usage stats')
@click.option('-b', '--bin', required=True, show_default=True, default="scg_compute_cost_monitor", type=click.Path(), help='Binary file path')
@click.option('-o', '--outdir', required=True, type=click.Path(), help='Output path')
def get_scg_cost_report(account, year, bin, plot,outdir):
    '''
    Get yearly SCG compute cost report for your lab
    '''
    
    # check if executable is found
    which_result = subprocess.run(['which', bin], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if which_result.returncode != 0:
        raise FileNotFoundError("Error: 'scg_compute_cost_monitor' not found.")

    # Initialize DataFrame
    data = pd.DataFrame(columns=['User', 'Hours', 'Cost', 'Month', 'Year'])  
    
    # Create the output dir if it doesn't exist
    outdir=f'{outdir}/{year}'
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # Loop through months
    for month in range(1, 13):
        # run the cost compute bash script
        click.echo(f'Getting compute usage for the month: {month}')
        command = f'{bin} -a {account} -m {month} -y {year}'
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        stdoutput, _ = process.communicate()

        # Parse usage data and append to DataFrame
        usage_lines = stdoutput.decode('utf-8').strip().split('\n')
        for line in usage_lines[1:]:  # Skip header
            user, hours, cost, month, year = line.split('\t')
            data = pd.concat([data, pd.DataFrame({'User': [user], 'Hours': [float(hours)], 'Cost': [float(cost)],
                                      'Month': [int(month)], 'Year': [int(year)]})], ignore_index=True)
    # Save the dataframe
    data.to_csv(f'{outdir}/scg_cost_report_{account}_{year}.tsv', sep='\t', index=False)

    if plot:
        # Group data by month and sum costs and generate plot
        monthly_costs = data.groupby('Month')['Cost'].sum().reset_index()
        plt.figure(figsize=(10, 6))
        plt.bar(monthly_costs['Month'], monthly_costs['Cost'])
        plt.title(f'Yearly Compute Usage Report {account} - {year}')
        plt.xlabel('Month')
        plt.ylabel('Total Cost (USD)')
        plt.xticks(range(1, 13))
        plt.tight_layout()
        plt.savefig(f'{outdir}/yearly_usage_{account}_{year}.png')
        plt.close()

        # Generate individual user usage plots for those 
        data = data[data['Cost'] != 0.0]
        unique_users = data['User'].unique()
        for user in unique_users:
            user_data = data[data['User'] == user]
            plt.figure(figsize=(10, 6))
            plt.bar(user_data['Month'], user_data['Cost'])
            plt.title(f'Usage Report for {user} - Year {year}')
            plt.xlabel('Month')
            plt.ylabel('Cost (USD)')
            plt.xticks(range(1, 13))
            plt.tight_layout()
            plt.savefig(f'{outdir}/user_usage_{user}_{year}.png')
            plt.close()

    click.echo(f'Compute usage report for the year {year} generated successfully!')

if __name__ == '__main__':
    get_scg_cost_report()
