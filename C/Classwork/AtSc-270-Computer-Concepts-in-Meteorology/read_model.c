// read_model.c
//
// Description: To take in a netcdf file and read in potential tempearture, perturbation
//              pressure, and base pressure from the file.  From these temperature and
//              pressure will be calculated, and those values will be printed to a text file.
//
// Input:  A netCDF file called "wrfout_d01_2008033100.nc"
//
// Output: Two text files containing pressure and temperature data called
//         "model_start.txt" (for 3/31/2008) and "model_end.txt" (for 4/1/2008)
//
//
// Compile: gcc -o read_model_exec read_model.c -L/usr/local/lib -lnetcdf -lm
//
// Written: April 2008, G. Mullendore
// Modifications:  Rewritten 4 April 2016, A. Neumann
// Modifications: Revised Lance Wilson, 2016 April 4
//

#include<netcdf.h>
#include<stdio.h>
#include<stdlib.h>
#include<math.h>

int main()
{
    // Declare variables
    int status;                  // status of netCDF calls
    int ncid;                    // netCDF file ID
    FILE *fout;                  // output file pointer
    int zid;                     // ID for vertical dimension
    size_t nz;                   // length of vertical dimension (number of height levels)
    int tid, pid, pbid;          // variable IDs
    size_t index[] = {0,0,4,9};  // location of value (4 element array!)
    float T, P, PB;              // variables from model (read from netCDF file)
    float theta;                 // potential temperature
    float temp, p;               // output variables

    int n, k;                    // loop counters for time and height
    int time;                    // Time variable

    // File outputs
    FILE *f_out;
    const char *output_name[] = {"model_start.txt","model_end.txt"};

    // Open file
    status = nc_open("wrfout_d01_2008033100.nc", 0, &ncid);
    if (status != NC_NOERR)
    {
        printf("Error occurred opening netCDF file. Exiting program.  Exiting program.\n");
        exit(1);
    }

    // Get vertical dimension ID
    nc_inq_dimid(ncid, "bottom_top", &zid);
    status = nc_inq_dimlen(ncid, zid, &nz);
    if (status != NC_NOERR)
    {
        printf("Error in loading vertical dimension ID. Exiting program.\n");
        exit(1);
    }
    printf("nz = %u\n",nz);

    // Get Temperature ID
    status = nc_inq_varid(ncid, "T", &tid);
    if (status != NC_NOERR)
    {
        printf("Error Occurred loading variable id for T. Exiting program.\n");
        exit(1);
    }

    // Get Perturbation pressure ID
    status = nc_inq_varid(ncid, "P", &pid);
    if (status != NC_NOERR)
    {
        printf("Error Occurred loading variable id for P. Exiting program.\n");
        exit(1);
    }

    // Get Base Pressure ID
    status = nc_inq_varid(ncid, "PB", &pbid);
    if (status != NC_NOERR)
    {
        printf("Error Occurred loading variable id for PB. Exiting program.\n");
        exit(1);
    }

    // Loop over time
    for (n = 0; n < 2; n++)
    {
        // First time through the loop time is 0
        if (n == 0)
            time = 0;
        // Otherwise (second time) the time is 8
        else
            time = 8;
        index[0] = time;

        // Open output file ("model_start.txt" the first time and "model_end.txt" the second
        if ((f_out = fopen(output_name[n], "w")) == NULL)
        {
            printf("Cannot open output file.\n");
            exit(1);
        }
        
        // Loop over height
        for (k = 0; k < nz; k++)
        {
            index[1] = k;
            // Load potential temperature
            status = nc_get_var1_float(ncid, tid, index, &T);
            if (status != NC_NOERR)
            {
                printf("Error loading variable potential temperature. Exiting program");
                exit(1);
            }

            // Load perturbation pressure
            status = nc_get_var1_float(ncid, pid, index, &P);
            if (status != NC_NOERR)
            {
                printf("Error loading variable perturbation pressure. Exiting program");
                exit(1);
            }

            // Retrieve base pressure
            status = nc_get_var1_float(ncid, pbid, index, &PB);
            if (status != NC_NOERR)
            {
                printf("Error loading variable base pressure. Exiting program");
                exit(1);
            }
            
            // Calculate temperature and pressure
            theta = T + 300; // Potential temp [K]
            p = P + PB;  // total Pressure [Pa]
            temp = theta * pow((p/1e5),(2.0/7.0));

            //Print to file
            fprintf(f_out, "%10f %10f\n", p/1e2, temp-273);

        } // End height (k) loop

        fclose(f_out);

    } // End time (n) loop

    // Close netCDF file
    nc_close(ncid);

}
