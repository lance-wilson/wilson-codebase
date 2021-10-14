// sonde_derive.c
//
// Purpose: Read in data from a radiosonde file and calculate values for helicity and 
// wind chill at valid heights and output the data to a file.
//
// Compile: gcc -o sonde_derive sonde_derive.c -lm
//
// Syntax: ./sonde_derive
//
// Input: radiosonde data (currently "BIS2016020712.txt") (changes must be specified below)
// 
// Output: height (m), helicity (m^2/s^2) (sonde_out.txt)
//         height (m), temperature (C), wind chill temperature (C) (sonde_out_ec.txt)
//
// Functions:  convert_temp: takes in the temperature value from the file and 
//                  divides by ten, then outputs.
//             radian_convert: takes in the wind direction and converts to radians.
//             convert_wind: takes in the wind value from file (which is in 
//                  decimeters per second), and outputs the value in meters per 
//                  second.
//             helicity_calc: takes in pointers to arrays for wind direction (in 
//                  radians), wind speed (m/s), height, u and v components of wind, 
//                  the integer array length, and the pointer to the array for helicity,
//                  and calculates the values of helicity and stores them in the helicity
//                  array. No return value.
//             calc_wind: takes in wind direction and speed, and a pointer to arrays 
//                  of wind components, converts wind to u and v coordinates, and 
//                  stores those values in the array. No return value.
//             vorticity: takes in pointers to arrays for winds (either u or v component),
//                  height, and wind speed, and the array index variable, and calculates
//                  vorticity at that level. Returns the value of vorticity.
//             fahren_temp: takes in pointers to temp and fahrenheit arrays, and the 
//                  integer array length, and converts the temperatures in fahrenheit.
//             toCelsius: takes in pointers to array for wind_chill and wind_chill_C and 
//                  the array length and converts the wind chills to degrees Celsius.
//             miles_wind: takes in pointers to arrays for wind_speed and wind_mph, 
//                  and the integer array length, and converts the wind speed from 
//                  meters per second to miles per hour.
//             wind_chill_calc: takes in pointers to arrays for temperature (in degrees 
//                  Fahrenheit), wind speed (in mph), wind chill, and the integer array 
//                  length, and calculates the wind chill at each height.
//
// Written: Lance Wilson, Feb 2016
//

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

double convert_temp(double temp_tenth);
double radian_convert(double wind_dir);
double convert_wind(double wind_speed_tenth);
void helicity_calc(double *wind_dir, double *wind_speed, double *height, int al, double *winds_u, double *winds_v, double *helicity);
void calc_wind(double wind_speed, double wind_dir, double *winds_u, double *winds_v, int g);
double vorticity(double *winds, double *height, int g, double *wind_speed);
void fahren_temp(double *temp, double *fahrenheit, int al);
void toCelsius(double *wind_chill, double *wind_chill_C, int al);
void miles_wind(double *wind_speed, double *wind_mph, int al);
void wind_chill_calc(double *temp, double *wind, double *wind_chill, int al);

int main() {

  // Input variables
  double *skip;
  double *pressure;	
  double *height;
  double *temp_tenth;
  double *dew_pt;   
  double *wind_dir;
  double *wind_speed_tenth;
  double *temp;                           
  double *wind_dir_rad;
  double *wind_speed; 
  double *winds_u;
  double *winds_v; 
  double *helicity;
  double *fahrenheit;
  double *wind_mph;
  double *wind_chill;  
  double *wind_chill_C;      
  char header[256];		// buffer for header lines
  const int header_length = 4;


  // Local variables
  const int max_al = 400;	// maximum array length
  int al = 0;			// actual array length
  int ap = 0;                   // array pointer
  int i, z;			// loop counter

  // File variables
  FILE *f_in;
  char *fname = "BIS2016020712.txt";
  char buff[256];		// buffer for file line read

  FILE *f_out, *f_out2;
  char *fname_out =  "sonde_out.txt";
  char *fname_out2 = "sonde_out_ec.txt";

  // Open input file
  if ((f_in = fopen(fname,"r"))==NULL) {
    printf("Cannot open input file.\n");
    exit(1);
  }

  // Allocate memory to store data arrays 
  //printf("The number of bytes in a double is %d.\n",sizeof(double));
  skip             = malloc(max_al * sizeof(double));
  pressure         = malloc(max_al * sizeof(double));
  height           = malloc(max_al * sizeof(double));
  temp_tenth       = malloc(max_al * sizeof(double));
  dew_pt           = malloc(max_al * sizeof(double));
  wind_dir         = malloc(max_al * sizeof(double));
  wind_speed_tenth = malloc(max_al * sizeof(double));
  temp             = malloc(max_al * sizeof(double));
  wind_dir_rad     = malloc(max_al * sizeof(double));
  wind_speed       = malloc(max_al * sizeof(double));
  winds_u          = malloc(max_al * sizeof(double));
  winds_v          = malloc(max_al * sizeof(double));
  helicity         = malloc(max_al * sizeof(double));
  fahrenheit       = malloc(max_al * sizeof(double));
  wind_mph         = malloc(max_al * sizeof(double));
  wind_chill       = malloc(max_al * sizeof(double));
  wind_chill_C     = malloc(max_al * sizeof(double));


  // Check allocation
  if ((skip==NULL) || (pressure==NULL) || (height==NULL) || (temp_tenth==NULL) || (dew_pt==NULL) || (wind_dir==NULL) || (wind_speed_tenth==NULL) || (wind_dir_rad==NULL) || (wind_speed==NULL) || (winds_u==NULL) || (winds_v==NULL) || (helicity==NULL) || (fahrenheit==NULL) || (wind_mph==NULL) || (wind_chill==NULL) || (wind_chill_C==NULL)) {
    printf("Error in memory allocation\n");
    exit(1);
  }

  // skip file header
  for (i=0; i<header_length; i++)
    fgets(buff,256,f_in);

  // Loop through file
  while(fgets(buff,256,f_in)) {
    // Read in data arrays
    al = al + 1;
    if (al > max_al)
    {
      printf("Warning: can not read entire input file:\n");
      printf("Reached end of allocated array space. (max_al = %d)\n",max_al);
      al = max_al;
      break; // breaks out of file read loop
    }
    // Read in all variables from file
    sscanf(buff,"%lf %lf %lf %lf %lf %lf %lf",&skip[ap],&pressure[ap],&height[ap],&temp_tenth[ap],&dew_pt[ap],&wind_dir[ap],&wind_speed_tenth[ap]);
    ap = ap + 1;
  }

  // Close input file
  fclose(f_in);

  // Open first output file
  if ((f_out = fopen(fname_out,"w"))==NULL) {
    printf("Cannot open output file.\n");
    exit(1);
  }
  // Open second output file
  if ((f_out2 = fopen(fname_out2,"w"))==NULL)
  {
    printf("Cannot open second output file.\n");
    exit(1);
  }


  // Convert tenths of variables to standard units and wind direction to radians.
  for (z=0; z<al; z++)
  {
    wind_dir_rad[z] = radian_convert(wind_dir[z]);
    wind_speed[z] = convert_wind(wind_speed_tenth[z]);
    temp[z] = convert_temp(temp_tenth[z]);

  }

  // Calculate helicity.
  helicity_calc(wind_dir_rad, wind_speed, height, al, winds_u, winds_v, helicity);

  // Write out height and helicity data to output file, using array indices, if data is valid.
  fprintf(f_out,"Height(m)\t\tHelicity(m^2/s^2)\n");
  for (i = 0; i < al; i++) {
    if(wind_speed_tenth[i] != 99999 || wind_dir[i] != 99999)
    {
      fprintf(f_out,"%.2lf  \t\t%.2lf\n",height[i],helicity[i]);
    }
  }

  // Calculate temperature in fahrenheit.
  fahren_temp(temp, fahrenheit, al);
  // Convert wind to MPH
  miles_wind(wind_speed, wind_mph, al);
  // Calculate wind chill
  wind_chill_calc(fahrenheit, wind_mph, wind_chill, al);
  // Convert wind chill back to Celsius
  toCelsius(wind_chill, wind_chill_C, al);

  // Write out height, temperature, and wind chill data to output file, if data is valid.
  fprintf(f_out2,"Height(m)\t\tTemp(C)\t\tWind Chill(C)\n");
  for (i = 0; i < al; i++)
  {
    if(temp_tenth[i] != 99999)
    {
      fprintf(f_out2,"%.2lf  \t\t%.2lf\t\t%.2lf\n",height[i],temp[i],wind_chill_C[i]);
    }
  }


  // Free allocated memory
  free(skip);
  free(pressure);
  free(height);
  free(temp_tenth);
  free(dew_pt);
  free(wind_dir);
  free(wind_speed_tenth);
  free(wind_dir_rad);
  free(temp);
  free(wind_speed);
  free(winds_u);
  free(winds_v);
  free(helicity);
  free(fahrenheit);
  free(wind_mph);
  free(wind_chill);  
  free(wind_chill_C);

  // Close output file
  fclose(f_out);
}  // End of main


// Converts temps from tenth of a degree to degree.
double convert_temp(double temp_tenth) 
{
  // declare local variables
  double temp;

  // convert from tenths of a degree to full degrees.
  temp = temp_tenth/10.0;

  return(temp);
}

// Converts the wind speed to radians.
double radian_convert(double wind_dir)
{
  double wind_rad;
  const double pi = 3.14159265358979;
  wind_rad = (wind_dir) * pi/180;
  return wind_rad;
}

// Converts wind speed from tenths of a m/s to m/s.
double convert_wind(double wind_speed_tenth)
{
  double wind_speed;
  wind_speed = wind_speed_tenth/10.0;
  return wind_speed;
}

// Calculates helicity
void helicity_calc(double *wind_dir, double *wind_speed, double *height, int al, double *winds_u, double *winds_v, double *helicity)
{
  int g;
  const int max_al = 400;
  double *vort_i;
  double *vort_j;

  // Allocate space for vorticity component arrays
  vort_i = malloc(max_al * sizeof(double));
  vort_j = malloc(max_al * sizeof(double));

  // Check allocation
  if ((vort_i==NULL) || (vort_j==NULL)) {
    printf("Error in memory allocation\n");
    exit(1);
  }

  // Calculate u and v components of wind
  for(g = 0; g < al; g++)
  {
    calc_wind(wind_dir[g], wind_speed[g], winds_u, winds_v, g);
  }

  // Calculate the i and j components of vorticity.
  for(g = 1; g < al; g++)
  {
    if (wind_speed[g] != 9999.9)
    {
      vort_i[g] = -1*(vorticity(winds_v, height, g, wind_speed));
      vort_j[g] = vorticity(winds_u, height, g, wind_speed);
    }
  }

  // Calculate helicity.
  for(g=0; g < al; g++)
  {
    helicity[g] = 0.5 * ((vort_i[g]*winds_u[g])+(vort_j[g]*winds_v[g]));
  }

  // Free memory
  free(vort_i);
  free(vort_j);
}

// Calculate u and v coordinates of the wind.
void calc_wind(double wind_dir, double wind_speed, double *winds_u, double *winds_v, int g)
{
  double u, v;
  u = -1 * wind_speed * sin(wind_dir);
  v = -1 * wind_speed * cos(wind_dir);
  winds_u[g] = u;
  winds_v[g] = v;
  return;
}

// Calculate components of vorticity.
double vorticity(double *winds, double *height, int g, double *wind_speed)
{
  int x = 1;
  while (wind_speed[g-x] == 9999.9)
  {
    x++;
  }
  double vorticity = (winds[g]-winds[g-x])/(height[g]-height[g-x]);
  return vorticity;
}

// Calculate temp in fahrenheit
void fahren_temp(double *temp, double *fahrenheit, int al)
{
  int m;
  for (m = 0; m < al; m++)
  {
    fahrenheit[m] = (temp[m] * 1.8) + 32;
  }
}

// Convert wind chill temperature from Fahrenheit to Celsius
void toCelsius(double *wind_chill, double *wind_chill_C, int al)
{
  int p;
  for (p = 0; p < al; p++)
  {
    wind_chill_C[p] = (wind_chill[p] - 32) * 5/9;
  }
}

// Convert temperature to fahrenheit
void wind_chill_calc(double *temp, double *wind, double *wind_chill, int al)
{
  int q;
  for (q = 0; q < al; q++)
  {
    wind_chill[q] = 35.74 + 0.6215 * temp[q] - 35.75*pow(wind[q],0.16) + 0.4275*temp[q]*pow(wind[q],0.16);
  }
}

// Convert wind speed to miles per hour
void miles_wind(double *wind_speed, double *wind_mph, int al)
{
  int n;
  for (n = 0; n < al; n++)
  {
    wind_mph[n] = wind_speed[n] * 2.23693629;
  }
}
