/*

 */

#include "G4PhysicalConstants.hh"
#include "G4SystemOfUnits.hh"

#include <getopt.h>
#include <cstdlib>
#include <queue>
#include <locale.h>
#include <cstdlib>
#include <iostream>
#include <ctime>


#include "G4UImanager.hh"
#include "G4UIterminal.hh"
#include "GateUIterminal.hh"
#include "G4UItcsh.hh"
#include "GateRunManager.hh"
#include "GateMessageManager.hh"
#include "GateSteppingVerbose.hh"
#include "GateRandomEngine.hh"
#include "GateApplicationMgr.hh"
#include "GateSourceMgr.hh"

#include "GateROOTBasicOutput.hh"
#include "TPluginManager.h"
#include "GateHitFileReader.hh"

#include "GateSourcePhaseSpace.hh"
#include "GateIAEAHeader.h"
#include "GateIAEARecord.h"
#include "GateIAEAUtilities.h"


FILE * pIAEAFile;
iaea_record_type *pIAEARecordType;
iaea_header_type *pIAEAheader;

// ----------------------------------------------------------------------------------
int OpenIAEAFile(G4String file)
{
  DD("OpenIAEAFile");
  G4String IAEAFileName  = file;
  G4String IAEAHeaderExt = ".IAEAheader";
  G4String IAEAFileExt   = ".IAEAphsp";

  if (pIAEAFile) fclose(pIAEAFile);
  pIAEAFile = 0;
  free(pIAEAheader);
  free(pIAEARecordType);
  pIAEAheader = 0;
  pIAEARecordType = 0;

  pIAEAFile = open_file(const_cast<char*>(IAEAFileName.c_str()),
                        const_cast<char*>(IAEAFileExt.c_str()),
                        (char*)"rb");
  if (!pIAEAFile) GateError("Error file not found: " + IAEAFileName + IAEAFileExt);

  pIAEAheader = (iaea_header_type *) calloc(1, sizeof(iaea_header_type));
  pIAEAheader->fheader = open_file(const_cast<char*>(IAEAFileName.c_str()),
                                   const_cast<char*>(IAEAHeaderExt.c_str()),
                                   (char*)"rb");

  if (!pIAEAheader->fheader)
    GateError("Error file not found: " + IAEAFileName + IAEAHeaderExt);

  if (pIAEAheader->read_header())
    GateError("Error reading phase space file header: " + IAEAFileName + IAEAHeaderExt);

  pIAEARecordType= (iaea_record_type *) calloc(1, sizeof(iaea_record_type));
  pIAEARecordType->p_file = pIAEAFile;
  pIAEARecordType->initialize();
  pIAEAheader->get_record_contents(pIAEARecordType);


  pIAEARecordType->read_particle();
  DD(pIAEARecordType->particle); // must be 1 for gamma

  return pIAEAheader->nParticles;
}
// ----------------------------------------------------------------------------------


//-----------------------------------------------------------------------------
int main( int argc, char* argv[] )
{

  // First of all, set the G4cout to our message manager
  GateMessageManager* theGateMessageManager = GateMessageManager::GetInstance();
  G4UImanager::GetUIpointer()->SetCoutDestination( theGateMessageManager );

#ifdef G4ANALYSIS_USE_ROOT
  // "Magic" line to avoid problem with ROOT plugin. It is useful when
  // compiling Gate on a given system and executing it remotely on
  // another (grid or cluster).  See
  // http://root.cern.ch/root/roottalk/roottalk08/0690.html
  // DS.
  gROOT->GetPluginManager()->AddHandler( "TVirtualStreamerInfo", "*", "TStreamerInfo", "RIO", "TStreamerInfo()" );
#endif

  // input param
  if (argc != 2) {
    std::cout << "Error: give filename as parameter" << std::endl;
    exit(0);
  }

  std::string filename = argv[1];
  DD(filename);

  // read input file
  int totalEventInFile = OpenIAEAFile(filename)-1;
  DD(totalEventInFile);

  // create root TTree
  G4String mSaveFilename = filename+".root";
  DD(mSaveFilename);
  auto pFile = new TFile(mSaveFilename, "RECREATE", "ROOT file for phase space", 9);
  auto pListeVar = new TTree("PhaseSpace", "Phase space tree");

  float x,y,z,dx,dy,dz,w,e;
  pListeVar->Branch("X", &x, "X/F");
  pListeVar->Branch("Y", &y, "Y/F");
  pListeVar->Branch("Z", &z, "Z/F");
  pListeVar->Branch("dX", &dx, "dX/F");
  pListeVar->Branch("dY", &dy, "dY/F");
  pListeVar->Branch("dZ", &dz, "dZ/F");
  pListeVar->Branch("Weight", &w, "Weight/F");
  pListeVar->Branch("Ekine", &e, "Ekine/F");

  // Loop particles
  std::srand(std::time(nullptr)); // use current time as seed for random generator
  int n=0;
  int non_gamma = 0;
  int k511 = 0;

  // totalEventInFile = 1e6;
  
  for(auto i=0 ; i<totalEventInFile; i++) {
    pIAEARecordType->read_particle();
    if (!pIAEARecordType->particle) break;
    if (pIAEARecordType->particle != 1) { // must be 1 for gamma
      //DD(pIAEARecordType->particle);
      //DD(i);
      // std::cout << "particle not gamma" << std::endl;
      // exit(0);
      non_gamma += 1;
    }
    else {
      // u v w for direction
      // x y z in cm for position
      // weight
      x = pIAEARecordType->x*cm;
      y = pIAEARecordType->y*cm;
      z = pIAEARecordType->z*cm;
      e = pIAEARecordType->energy;
      dx = pIAEARecordType->u;
      dy = pIAEARecordType->v;
      dz = pIAEARecordType->w;
      w = pIAEARecordType->weight;
      const double tol = 1e-5;
      if (e >= 0.5110034-tol and e <= 0.5110034+tol)  {
        k511 += 1;
        // double ee = e;
        // e = 0.5105 + (double)std::rand()/(double)RAND_MAX/1000;
        // std::cout << "e = " << std::endl;
      }
      else {
        pListeVar->Fill();
        n++;
      }
    }
  }
  std::cout << "Found " << n << std::endl;
  std::cout << "Non gamma " << non_gamma << std::endl;
  std::cout << "511 " << k511 << std::endl;

  // clean
  pFile->Write();
  pFile->Close();
  fclose(pIAEAFile);

  return 0;
}
//-----------------------------------------------------------------------------
