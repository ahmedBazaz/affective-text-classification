#!/usr/bin/perl -w
# Evaluates emotion system performance
use strict;

if (!$ARGV[0] || !$ARGV[1]) {
  print "Usage: $0 <gold standard> <system output>\n\n";
  print "Sample: $0 trial/affectivetext_trial.emotions.gold.key trial/sample.output\n\n";
  exit;
}

my $gold = $ARGV[0];
my $output = $ARGV[1];

# Load the gold standard.
my %stats = (); # $emotion -> $id -> $hit
my %tps = ();  # $emotion => $true positives
my %fps = ();  # $emotion => $false positives
my %tns = ();  # $emotion => $true negatives
my %fns = ();  # $emotion => $false negatives
my $num_instance = 0;
open(IN, $gold) or die("Cannot open $gold");
while (my $line = <IN>) {
  chomp($line);
  my ($id, @emotions) = split(/\s+/, $line);
  foreach my $emotion (@emotions) {
    $stats{$emotion}{$id} = 0;
    $tps{$emotion} = 0;
    $fps{$emotion} = 0;
    $tns{$emotion} = 0;
    $fns{$emotion} = 0;
  }
  ++$num_instance;
}
close(IN);

# Load the system output.
open(IN, $output) or die("Cannot open $output");
while (my $line = <IN>) {
  chomp($line);
  my ($id, @emotions) = split(/\s+/, $line);
  foreach my $emotion (@emotions) {
    if (exists $stats{$emotion}{$id}) {
      ++$tps{$emotion};
      $stats{$emotion}{$id} = 1;
    } else {
      ++$fps{$emotion};
    }
  }
}
close(IN);

# Compute true and false negatives.
my $num_emotions = 0;
foreach my $emotion (keys %stats) {
  ++$num_emotions;
  foreach my $id (keys %{$stats{$emotion}}) {
    if ($stats{$emotion}{$id} == 0) {
      ++$fns{$emotion};
    }
  }
  $tns{$emotion} = $num_instance - $tps{$emotion} - $fps{$emotion} - $fns{$emotion};
}

# Compute acc, precision, recall.
my $sum_accuracy = 0;
my $sum_precision = 0;
my $sum_recall = 0;
my $sum_fscore = 0;
foreach my $emotion (keys %stats) {
  my $accuracy = ($tps{$emotion} + $tns{$emotion}) / ($num_instance);

  my $precision = 0;
  if ($tps{$emotion} + $fps{$emotion} > 0) {
    $precision = $tps{$emotion} / ($tps{$emotion} + $fps{$emotion});
  }

  my $recall = 0;
  if ($tps{$emotion} + $fns{$emotion} > 0) {
    $recall = $tps{$emotion} / ($tps{$emotion} + $fns{$emotion});
  }

  my $fscore = 0;
  if ($recall + $precision > 0) {
    $fscore = (2 * $recall * $precision) / ($recall + $precision);
  }

  printf "$emotion, ACC: %.4f, PREC: %.4f, REC: %.4f, F: %.4f\n", $accuracy, $precision, $recall, $fscore;

  $sum_accuracy += $accuracy;
  $sum_precision += $precision;
  $sum_recall += $recall;
  $sum_fscore += $fscore;
}

printf "Average, ACC: %.4f, PREC: %.4f, REC: %.4f, F: %.4f\n", ($sum_accuracy/$num_emotions), ($sum_precision/$num_emotions), ($sum_recall/$num_emotions), ($sum_fscore/$num_emotions);

