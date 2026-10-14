import matplotlib.pyplot as plt
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

genetic_code = {
    "UUU": "Phe", "UUC": "Phe", "UUA": "Leu", "UUG": "Leu",
    "UCU": "Ser", "UCC": "Ser", "UCA": "Ser", "UCG": "Ser",
    "UAU": "Tyr", "UAC": "Tyr", "UAA": "Stop", "UAG": "Stop",
    "UGU": "Cys", "UGC": "Cys", "UGA": "Stop", "UGG": "Trp",
    "CUU": "Leu", "CUC": "Leu", "CUA": "Leu", "CUG": "Leu",
    "CCU": "Pro", "CCC": "Pro", "CCA": "Pro", "CCG": "Pro",
    "CAU": "His", "CAC": "His", "CAA": "Gln", "CAG": "Gln",
    "CGU": "Arg", "CGC": "Arg", "CGA": "Arg", "CGG": "Arg",
    "AUU": "Ile", "AUC": "Ile", "AUA": "Ile", "AUG": "Met",
    "ACU": "Thr", "ACC": "Thr", "ACA": "Thr", "ACG": "Thr",
    "AAU": "Asn", "AAC": "Asn", "AAA": "Lys", "AAG": "Lys",
    "AGU": "Ser", "AGC": "Ser", "AGA": "Arg", "AGG": "Arg",
    "GUU": "Val", "GUC": "Val", "GUA": "Val", "GUG": "Val",
    "GCU": "Ala", "GCC": "Ala", "GCA": "Ala", "GCG": "Ala",
    "GAU": "Asp", "GAC": "Asp", "GAA": "Glu", "GAG": "Glu",
    "GGU": "Gly", "GGC": "Gly", "GGA": "Gly", "GGG": "Gly",
}


def codon_to_aminoacid(codon):
    codon = codon.upper().replace("T", "U")
    return genetic_code[codon]



def read_fasta(filename):
    sequence = ""
    for line in open(filename):
        if not line.startswith(">"):
            sequence += line.strip()
    return sequence.upper().replace("T", "U")   


rna = read_fasta("sars_cov2_NC_045512.2.fasta")
print("Genome length:", len(rna))


counts = {}
for frame in range(3):
    for i in range(frame, len(rna) - 2, 3):
        codon = rna[i:i + 3]
        if codon in genetic_code:
            counts[codon] = counts.get(codon, 0) + 1

sorted_codons = sorted(counts.items(), key=lambda x: x[1], reverse=True)
top10 = sorted_codons[:10]

print("\nTop 10 codons:")
for codon, count in top10:
    print(codon, codon_to_aminoacid(codon), count)

labels = [codon + "\n" + codon_to_aminoacid(codon) for codon, count in top10]
values = [count for codon, count in top10]
plt.bar(labels, values)
plt.title("Top 10 most frequent codons")
plt.ylabel("Frequency")
plt.savefig("top10_codons.png")
plt.show()

# ---------------- Ex 3: Prompt for the AI ----------------
aminoacids = []
for codon, count in top10:
    aa = codon_to_aminoacid(codon)
    if aa != "Stop" and aa not in aminoacids:
        aminoacids.append(aa)

prompt = ("The 10 most frequent codons in my genome are: "
          + ", ".join(codon + " (" + codon_to_aminoacid(codon) + ")" for codon, count in top10)
          + ". Make a list of foods that contain the lowest amounts of these amino acids: "
          + ", ".join(aminoacids) + ".")

print("\nPrompt for the AI:\n" + prompt)
