using System;
using System.Numerics;

class Simulation
{
    static double RadialWaveFunction(int n, int l, double r)
    {
        double rho = 2.0 * r / n;
        double L = Math.Pow(rho, l) * Math.Exp(-rho / 2);

        double laguerre = LaguerrePolynomial(n - l - 1, 2 * l + 1, rho);

        return Math.Sqrt((2.0 / n) * Math.Pow(2.0 / n, l + 1)) * L * laguerre;
    }

    static double LaguerrePolynomial(int k, int a, double x)
    {
        if (k == 0) return 1.0;
        else if (k == 1) return 1.0 + a - x;
        else
            return ((2 * k + a - 1 - x) * LaguerrePolynomial(k - 1, a, x) -
                    (k - 1 + a)         * LaguerrePolynomial(k - 2, a, x)) / k;
    }

    /* https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Supplemental_Modules_(Physical_and_Theoretical_Chemistry)/Quantum_Mechanics/10%3A_Multi-electron_Atoms/Electronic_Angular_Wavefunction */
    static Complex AngularWaveFunction(int l, int m, double theta, double phi)
    {
        double Plm = AssociatedLegendrePolynomial(l, m, Math.Cos(theta));
        Complex Ylm = Math.Sqrt((2 * l + 1) / (4 * Math.PI) *
                                Factorial(l - m) / Factorial(l + m)) *
                                Plm * Complex.Exp(new Complex(0, m * phi));

        return Ylm;
    }

    /* 
       https://chem.libretexts.org/Ancillary_Materials/Reference/Reference_Tables/Mathematical_Functions/M2%3A_Legendre_Polynomials

       archive:  https://web.archive.org/web/20170811064758/http://www.scielo.org.co/pdf/racefn/v37n145/v37n145a09.pdf
       original: http://www.scielo.org.co/pdf/racefn/v37n145/v37n145a09.pdf 
    */
    static double AssociatedLegendrePolynomial(int l, int m, double x)
    {
        /*
        function pnm = flgndr(z,n)
            nz  = length(z);
            pnm = zeros(nz,n+1);
            fac = prod(2:n);

            sqz2   = sqrt((1.0-z.*z));
            hsqz2  = 0.5*sqz2;
            ihsqz2 = z./hsqz2;

            if(n==0)
                pnm(:,1) = 1.0;
                return
            end

            if(n==1)
                pnm(:,1) = -0.5*sqz2;
                pnm(:,2) = z;
                pnm(:,3) = sqz2;
                return
            end
            
            pnm(:,1) = (1-2*abs(n-2*floor(n/2)))*hsqz2.^n/fac;
            pnm(:,2) = -pnm(:,1)*n.*ihsqz2;
            for mr=1:2*n-1
                pnm(:,mr+2)=(mr-n).*ihsqz2.
            *pnm(:,mr+1)-(2*n-mr+1)*mr*pnm(:,mr);
            
            end
        end
        */

        double P0 = 1.0;
        double P1 = x;

        for (int k = 2; k <= l; k++)
        {
            double Pk = ((2 * k - 1) * x * P1 - (k + m - 1) * P0) / (k - m);
            P0 = P1;
            P1 = Pk;
        }

        return P1;
    }

    static int Factorial(int n)
    {
        if (n == 0)
            return 1;

        int result = 1;
        for (int i = 1; i <= n; i++) result *= i;

        return result;
    }

    public static void Simulate()
    {
        int n = 2; // principal quantum number
        int l = 1; // angular momentum quantum number
        int m = 0; // magnetic quantum number

        int    gridSize  = 30;
        double maxRadius = 1;

        double[,] waveFunctionValues = new double[gridSize, gridSize];
        double    deltaRadius        = maxRadius / gridSize;

        for (int i = 0; i < gridSize; i++)
        {
            double r = i * deltaRadius;

            for (int j = 0; j < gridSize; j++)
            {
                double theta = Math.PI * j / gridSize;
                double phi   = 0.0;

                double  radialPart  = RadialWaveFunction(n, l, r);
                Complex angularPart = AngularWaveFunction(l, m, theta, phi);

                double psi = radialPart * radialPart *
                             angularPart.Magnitude * angularPart.Magnitude;

                waveFunctionValues[i, j] = psi;

                Console.WriteLine(psi + ",");
            }
        }
    }
}
