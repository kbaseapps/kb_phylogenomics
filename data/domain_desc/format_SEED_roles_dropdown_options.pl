#!/usr/bin/perl


open (FUNCAT_FILE, 'SEED_funcat.txt');

while (<FUNCAT_FILE>) {
    chomp;
    ($funcat, $seed_role) = split (/\t/);
    $seed_role_with_spaces = $seed_role;
    $seed_role_with_spaces =~ s/\_/ /g;

    print join ("\n", 
	"\t\t".'{', 
	"\t\t\t".'"value": "SEED: '.$seed_role.'",',
	"\t\t\t".'"display": "SEED: '.$funcat.': '.$seed_role_with_spaces.'",',
	"\t\t\t".'"id": "SEED: '.$seed_role.'",',
	"\t\t\t".'"ui-name": "SEED: '.$seed_role.'"',
	"\t\t".'},')."\n";
}
close (FUNCAT_FILE);
