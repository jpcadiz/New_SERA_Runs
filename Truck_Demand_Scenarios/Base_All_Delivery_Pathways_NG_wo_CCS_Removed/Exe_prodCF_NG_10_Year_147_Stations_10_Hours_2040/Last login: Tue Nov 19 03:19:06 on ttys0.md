Last login: Tue Nov 19 03:19:06 on ttys000
(base) jbpcadiz@Johns-MacBook-Pro-94 ~ % ssh jpcadiz@hpcsh.nrel.gov

*****************************************************************************

                         NOTICE TO USERS

This is a Federal computer or information system and is the property
of the United States Government.  It is for authorized use only.
By using this information system, or connecting any device to this
information system, the user acknowledges, understands and consents
to certain identified actions and agrees:

  * that user has no reasonable expectation of privacy regarding
    communications or data transmitted or stored on this information
    system or any devices connected to this information system.

  * that any or all uses of this information system and all files
    transmitted, stored or connected to this information system may
    be intercepted, monitored, recorded, copied and searched and may
    be used or disclosed to law enforcement or other Government
    agencies, as deemed appropriate by the Department of Energy
    or as mandated by law.

  * to be bound by the requirements for use of Government information
    systems consistent with DOE Order 203.1 and any other applicable
    DOE Order or directive regarding use of DOE information systems.

  * that any unauthorized or improper use of Government information
    systems may result in limitations placed on the use of Government
    information systems, disciplinary or adverse actions, criminal
    penalties, and/or financial liability for the cost of such
    improper use.

To the extent that the user has any questions concerning the use of
Government information systems, the user should consult with their
supervisor or other appropriate management personnel.

  LOG OFF IMMEDIATELY if you do not agree to the conditions
  stated in this warning.

*****************************************************************************

(jpcadiz@hpcsh.nrel.gov) Password+OTPToken: 
(jpcadiz@hpcsh.nrel.gov) Password+OTPToken: 


This NREL High-Performance Computing Center system
may only contain data related to scientific research.

This system may only contain data that is
categorized as:
  low
  non-sensitive

This system may not store or process data that is:
  proprietary
  export controlled

By logging into this system, you agree to the
HPC Center terms and policies:
  https://www.nrel.gov/hpc/policies.html

 *** Notice: Mail List for Support requests ***

Send email to hpc-help@nrel.gov for HPC support
requests and trouble reports.

For workstation and laptop service requests:
  service.center@nrel.gov  303-275-4171


\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/

  DISK QUOTA

  This system is intended as a jump host only.
  No data is allowed to be stored on this system.
  Disk usage quotas will be strictly enforced.

  500Mb per user. No exceptions.

  Please use Globus Connect to facilitate any file transfers.
             --------------

/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

Last failed login: Tue Nov 19 06:44:17 EST 2024 from 168.150.102.4 on ssh:notty
There was 1 failed login attempt since the last successful login.
Last login: Tue Nov 19 06:22:57 2024 from 168.150.102.4
[jpcadiz@hpcsh ~]$ ssh kestrel.hpc.nrel.gov

*****************************************************************************

                         NOTICE TO USERS

This is a Federal computer or information system and is the property of the
United States Government.  It is for authorized use only.  By using this
information system, or connecting any device to this information system, the
user acknowledges, understands and consents to certain identified actions and agrees:

  * that user has no reasonable expectation of privacy regarding communications
    or data transmitted or stored on this information system or any devices
    connected to this information system.

  * that any or all uses of this information system and all files transmitted,
    stored or connected to this information system may be intercepted, monitored,
    recorded, copied and searched and may be used or disclosed to law enforcement
    or other Government agencies, as deemed appropriate by the Department of Energy
    or as mandated by law. 

  * to be bound by the requirements for use of Government information systems
    consistent with DOE Order 203.1 and any other applicable DOE Order or directive
    regarding use of DOE information systems.  

  * that any unauthorized or improper use of Government information systems may
    result in limitations placed on the use of Government information systems,
    disciplinary or adverse actions, criminal penalties, and/or
    financial liability for the cost of such improper use.

To the extent that the user has any questions concerning the use of Government
information systems, the user should consult with their supervisor or other
appropriate management personnel.  LOG OFF IMMEDIATELY if you do not agree
to the conditions stated in this warning.

*****************************************************************************

jpcadiz@kestrel.hpc.nrel.gov's password: 


The NREL High Performance Computing Center systems
may only contain data related to scientific research.

This system may only contain data that is categorized as:
  low
  non-sensitive

This system may not store or process data that is:
  proprietary
  export controlled

By logging into this system, you agree to the HPC Center terms and policies:
  https://www.nrel.gov/hpc/policies.html

 *** Notice: Mail List for Support requests ***

Send email to hpc-help@nrel.gov for HPC support requests and trouble reports.

Contact the NREL Service Center For workstation and laptop service requests:
  service.center@nrel.gov  303-275-4171


Last login: Tue Nov 19 04:23:28 2024 from 10.60.127.204


The NREL High Performance Computing Center systems
may only contain data related to scientific research.

This system may only contain data that is categorized as:
  low
  non-sensitive

This system may not store or process data that is:
  proprietary
  export controlled

By logging into this system, you agree to the HPC Center terms and policies:
  https://www.nrel.gov/hpc/policies.html

 *** Notice: Mail List for Support requests ***

Send email to hpc-help@nrel.gov for HPC support requests and trouble reports.

Contact the NREL Service Center For workstation and laptop service requests:
  service.center@nrel.gov  303-275-4171


[jpcadiz@kl2 ~] CPU $ ls
bin      git-lfs-3.5.1                    SERA2.0-ExternalUsers
git-lfs  git-lfs-linux-386-v3.5.1.tar.gz  SERA-Runs
[jpcadiz@kl2 ~] CPU $ cd SERA-Runs
[jpcadiz@kl2 SERA-Runs] CPU $ ls
Exe_prodCF_NG_10  Exe_prodCF_NG_5_example  SERA-Runs
[jpcadiz@kl2 SERA-Runs] CPU $ cd SERA-Runs
[jpcadiz@kl2 SERA-Runs] CPU $ ls
 Exe_prodCF_NG_10                              'GitHub Token.rtf'
 Exe_prodCF_NG_15                               SERA-Runs
 Exe_prodCF_NG_5                                SERAWalkthrough_Chris.txt
 Exe_prodCF_NG_5_example                        test-cases
 Exe_prodCF_NG_5_example_copy_refamiliarizing   test-cases.zip
[jpcadiz@kl2 SERA-Runs] CPU $ sbatch /Exe_prodCF_NG_5/scen_SERA.sbatch
sbatch: error: Unable to open file /Exe_prodCF_NG_5/scen_SERA.sbatch
[jpcadiz@kl2 SERA-Runs] CPU $ sbatch home/jpcadiz/SERA-Runs/Exe_prodCF_NG_5/scen_SERA.sbatch
sbatch: error: Unable to open file home/jpcadiz/SERA-Runs/Exe_prodCF_NG_5/scen_SERA.sbatch
[jpcadiz@kl2 SERA-Runs] CPU $ sbatch /home/jpcadiz/SERA-Runs/Exe_prodCF_NG_5/scen_SERA.sbatch
sbatch: error: Unable to open file /home/jpcadiz/SERA-Runs/Exe_prodCF_NG_5/scen_SERA.sbatch
[jpcadiz@kl2 SERA-Runs] CPU $ sbatch /home/jpcadiz/SERA-Runs/SERA-Runs/Exe_prodCF_NG_5/scen_SERA.sbatch
Submitted batch job 6069869
[jpcadiz@kl2 SERA-Runs] CPU $ sbatch /home/jpcadiz/SERA-Runs/SERA-Runs/Exe_prodCF_NG_10/scen_SERA.sbatch
Submitted batch job 6069870
[jpcadiz@kl2 SERA-Runs] CPU $ sbatch /home/jpcadiz/SERA-Runs/SERA-Runs/Exe_prodCF_NG_15/scen_SERA.sbatch
Submitted batch job 6069871
[jpcadiz@kl2 SERA-Runs] CPU $ 
