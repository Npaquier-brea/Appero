#include <iostream>
#include <unistd.h>
#include <thread>
#include <fstream>

int main(void)
{
    unsigned int nthreads = std::thread::hardware_concurrency();
    std::string const nomFichier("nbrThreads.txt");
    std::ofstream monFlux(nomFichier.c_str());
    if (monFlux)
    {
        monFlux << nthreads << std::endl;
        monFlux.close();
    }
    else
    {
        std::cout << "ERREUR: Impossible d'ouvrir le fichier." << std::endl;
    }
    return 0;
}