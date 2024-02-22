from math import ceil
import glob
import os



def get_fna_chunks(wildcards):
    # Get the file path
    get_chunk_num = checkpoints.calculate_db_chunks.get(**wildcards).output[0]
    split_dir = os.path.split(get_chunk_num)[0]

    return expand(os.path.join(split_dir, "chunk_{chunk_num}.fna"),chunk_num=glob_wildcards(os.path.join(split_dir, "chunk_{chunk_num}.fna")).chunk_num)

def get_index_db_chunks(wildcards):
    # Get the file path
    get_chunk_num = checkpoints.calculate_db_chunks.get(**wildcards).output[0]
    split_dir = os.path.split(get_chunk_num)[0]

    return expand(os.path.join(config['params']['align']['bwa2']['db'], "index", config['params']['project'], "chunk_{chunk_num}/chunk_{chunk_num}.amb"),chunk_num=glob_wildcards(os.path.join(split_dir, "chunk_{chunk_num}.fna")).chunk_num)


def get_db_chunk_alignments(wildcards):
    # Get the file path
    get_chunk_num = checkpoints.calculate_db_chunks.get(**wildcards).output[0]
    split_dir = os.path.split(get_chunk_num)[0]

    return expand(
        os.path.join(
            config["output"]["classifier"],"bwa_align/{sample}/Aligned.BWA.chunk_{chunk_num}.sortedByCoord.mapped.out.bam"),
        sample=wildcards.sample,
        chunk_num=glob_wildcards(os.path.join(split_dir, "chunk_{chunk_num}.fna")).chunk_num
    )


rule download_taxdump:
    input:
        candidate_species =  os.path.join(
                config["output"]["classifier"],
                "rmhost_kraken2_qc/study/krak_candidate_species.txt"),
    output:
        assembly_summary = expand(os.path.join(
            config["params"]["align"]["download_dir"],
            "taxonomy/{domain}_assembly_summary.txt"),
            domain=['bacteria','fungi','viral','archaea']),
        taxdump = expand(os.path.join(
            config["params"]["align"]["download_dir"],
            "taxonomy/{taxdump}"),
            taxdump=["names.dmp", "nodes.dmp","merged.dmp"]),
    params:
        taxonomy_folder = os.path.join(
            config["params"]["align"]["download_dir"],
            "taxonomy"),
    resources:
        mem_mb = 1000,
    threads:
        1
    run:
        import os
        import pandas as pd

        domains = ['bacteria','archaea','fungi','viral']

        for domain in domains:
            if not os.path.exists(os.path.join(params.taxonomy_folder,str(domain)+"_assembly_summary.txt")):
                shell("wget -q https://ftp.ncbi.nlm.nih.gov/genomes/refseq/{domain}/assembly_summary.txt -O {params.taxonomy_folder}/{domain}_assembly_summary.txt")
                print(f"{domain} assembly summary downloaded successfully.")

        shell("wget -q https://ftp.ncbi.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.tar.gz -O {params.taxonomy_folder}/new_taxdump.tar.gz")
        shell("tar -xf {params.taxonomy_folder}/new_taxdump.tar.gz -C {params.taxonomy_folder}")
        if os.path.exists(os.path.join(params.taxonomy_folder, "new_taxdump.tar.gz")): 
            os.remove(os.path.join(params.taxonomy_folder, "new_taxdump.tar.gz"))

rule download_candidate_species:
    input:
        candidate_species =  os.path.join(
                config["output"]["classifier"],
                "rmhost_kraken2_qc/study/krak_candidate_species.txt"),
        assembly_summary = expand(os.path.join(
            config["params"]["align"]["download_dir"],
            "taxonomy/{domain}_assembly_summary.txt"),
            domain=['bacteria','fungi','viral','archaea']),
        taxdump = expand(os.path.join(
            config["params"]["align"]["download_dir"],
            "taxonomy/{taxdump}"),
            taxdump=["names.dmp", "nodes.dmp","merged.dmp"])
    output:
        library_fna = os.path.join(
            config["params"]["align"]["download_dir"],
            "library/library.fna"),
        interest_fna = temp(os.path.join(
            config["params"]["align"]["download_dir"],
            "library/",f"{config['params']['project']}.fna")),
        acc2tax = os.path.join(
           config["params"]["align"]["download_dir"],
            f"acc2tax/{config['params']['project']}_acc2tax.txt"),                                  
    params:
        download_path = os.path.join(
            config["params"]["align"]["download_dir"],),
        download_candidate_species_script= config["scripts"]["download_candidate_species"],
        library_report_path = os.path.join(
            config["params"]["classifier"]["kraken2uniq"]["kraken2_database"],
                                    "library_report.tsv"),
        seqid2taxid_path = os.path.join(config["params"]["classifier"]["kraken2uniq"]["kraken2_database"],
                                    "seqid2taxid.map"),
        project = config["params"]["project"],
    log:
        os.path.join(config["logs"]["classifier"],
                    "bowtie2_db/download_fasta.log")
    resources:
        mem_mb = 1000,
    threads:
        config["resources"]["download_candidate_species"]["threads"]
    shell:
        '''
        python  {params.download_candidate_species_script}\
        --candidate {input.candidate_species} \
        --folder {params.download_path} \
        --seqid2taxid {params.seqid2taxid_path} \
        --library_report {params.library_report_path} \
        --interest_fna {output.interest_fna} \
        --library_fna {output.library_fna} \
        --project {params.project} \
        --log_file {log} \
        --acc2tax {output.acc2tax} \
        --processors {threads} \
        '''

if config["params"]["align"]["bowtie2"]["do"]:
    rule bowtie2_build_Index:
        output:
            expand(
                config['params']['align']['bowtie2']['db'],"/index/",config['params']['project'],"/",config['params']['project'],{{ext}},
                ext=[
                    ".1.bt2",
                    ".2.bt2",
                    ".3.bt2",
                    ".4.bt2",
                    ".rev.1.bt2",
                    ".rev.2.bt2",
                ],
            )
        input:
            interest_fna = os.path.join(
                config["params"]["align"]["download_dir"],
                f"library/{config['params']['project']}.fna"),
        params:
            bowtie2_db_name = os.path.join(
                config["params"]["align"]["bowtie2"]["db"],
                f"index/{config['params']['project']}/{config['params']['project']}")
        # conda:
        #     "../envs/bowtie2.yaml"
        threads: 40
        log:
            os.path.join(config["logs"]["classifier"],
                        "bowtie2_db/bowtie2_db_build.log")
        shell:
            "bowtie2-build --threads {threads} {input.interest_fna} --offrate 0.5 {params.bowtie2_db_name} > {log} 2>&1"
    rule bowtie2_alignment:
        output:
            bowtie2_aligned_bam= os.path.join(
                config["output"]["classifier"],"bowtie2_align/{sample}/Aligned_bowtie2.bam"),
            bowtie2_aligned_bam_index = os.path.join(
                config["output"]["classifier"],"bowtie2_align/{sample}/Aligned_bowtie2.bam.bai"),
        input:
            krak2_extracted_bam = os.path.join(
                config["output"]["classifier"],
                "rmhost_extracted_classified_output/{sample}/{sample}_kraken2_extracted_classified.bam"),
            db=rules.bowtie2_build_Index.output,
            krak_screened_fastq = os.path.join(
                config["output"]["classifier"],
                "rmhost_extracted_classified_output/{sample}/{sample}_kraken2_screen.fastq"),
            krak_screened_r1_fastq = os.path.join(
                config["output"]["classifier"],
                "rmhost_extracted_classified_output/{sample}/{sample}_kraken2_screen_r1.fastq"),
            krak_screened_r2_fastq = os.path.join(
                config["output"]["classifier"],
                "rmhost_extracted_classified_output/{sample}/{sample}_kraken2_screen_r2.fastq")
        params:
            bowtie2_db_name = os.path.join(
                config["params"]["align"]["bowtie2"]["db"],
                f"index/{config['params']['project']}/{config['params']['project']}")
        threads: 30
        log:
            os.path.join(config["logs"]["classifier"],
                        "bowtie2/{sample}/bowtie2_alignment.log")
        # conda:
        #     "../envs/bowtie2.yaml"
        benchmark:
            os.path.join(config["benchmarks"]["classifier"],
                "bowtie2/{sample}/bowtie2_alignment.tsv")
        shell:
            """
            if [ -s "{input.krak_screened_fastq}" ]; then
                bowtie2 -x {params.bowtie2_db_name} --local -a --threads {threads} --very-sensitive -U {input.krak_screened_fastq}  | samtools sort -O bam > {output.bowtie2_aligned_bam}
            else
                bowtie2 -x {params.bowtie2_db_name} --local -a --threads {threads} --very-sensitive -1 {input.krak_screened_r1_fastq} -2 {input.krak_screened_r2_fastq}  | samtools sort --threads {threads} -O bam > {output.bowtie2_aligned_bam}
            fi

            samtools index {output.bowtie2_aligned_bam}
            """
    rule bowtie2_lca_classifier:
        input:
            bowtie2_aligned_bam= os.path.join(
                            config["output"]["classifier"],"bowtie2_align/{sample}/Aligned_bowtie2.bam"),
            taxonomy_db = os.path.join(
                                        config["params"]["align"]["download_dir"],
                                        "ncbi.pkl"),
            acc2tax_db = os.path.join(config["params"]["align"]["download_dir"],f"{config['params']['project']}.db","IDENTITY"),
            interest_fna = temp(os.path.join(
            config["params"]["align"]["download_dir"],
            f"library/{config['params']['project']}.fna")),
        output:
            lca_profile = os.path.join(
                config["output"]["classifier"],"bowtie2_align/{sample}/Aligned_bowtie2.sam2lca.csv"),
            lca_bam = os.path.join(
                config["output"]["classifier"],"bowtie2_align/{sample}/Aligned_bowtie2.sam2lca.bam"),
            # bowtie2_aligned_cleaned_bam= temp(os.path.join(
            #     config["output"]["classifier"],"bowtie2_align/{sample}/Aligned_bowtie2_cleaned.sam2lca.bam")),    
        params:
            sam2lca_db_name = os.path.join(
                config["params"]["align"]["download_dir"],),
            bowtie2_output = os.path.join(
                config["output"]["classifier"],"bowtie2_align","{sample}"),
            base_name = "Aligned_bowtie2",
            project = PROJECT
        shell:
            """
            cd {params.bowtie2_output}

            sam2lca --dbdir {params.sam2lca_db_name} analyze -b -i 0.8 -a {params.project} ./Aligned_bowtie2.bam
            """
    rule bowtie2_aligned_all:
        input:
            # expand(os.path.join(
            #     config["output"]["profile"],
            #     "{sample}/microbiome_out/barcodes.tsv"),sample=SAMPLES_ID_LIST),
            # expand(os.path.join(
            #     config["output"]["profile"],
            #     "{sample}/microbiome_out/matrix.mtx"),sample=SAMPLES_ID_LIST),
            # expand(os.path.join(
            #     config["output"]["profile"],
            #     "{sample}/microbiome_out/features.tsv"),sample=SAMPLES_ID_LIST)
            expand(os.path.join(
                config["output"]["classifier"],"bowtie2_align/{sample}/Aligned_bowtie2.sam2lca.csv"),sample=SAMPLES_ID_LIST)

else:
    rule bowtie2_aligned_all:
        input:

if config["params"]["align"]["bwa"]["do"]:
    rule bwa_build_Index:
        output:
            expand(
                f"{config['params']['align']['bwa']['db']}/index/{config['params']['project']}/{config['params']['project']}{{ext}}",
                ext=[
                    ".amb",
                    ".ann",
                    ".bwt",
                    ".pac",
                    ".sa"
                ],
            )
        input:
            interest_fna = os.path.join(
                config["params"]["align"]["download_dir"],
                f"library/{config['params']['project']}.fna"),
        params:
            bwa_db_name = os.path.join(
                config["params"]["align"]["bwa"]["db"],
                f"index/{config['params']['project']}/{config['params']['project']}")
        # conda:
        #     "../envs/bowtie2.yaml"
        threads: 20
        log:
            os.path.join(config["logs"]["classifier"],
                        "bwa_db/bwa_db_build.log")
        shell:
            """
            bwa index {input.interest_fna} -p {params.bwa_db_name}
            """
    rule bwa_alignment:
        output:
            bwa_aligned_sorted_bam = os.path.join(
                config["output"]["classifier"],"bwa_align/{sample}/Aligned.BWA.sortedByCoord.out.bam"),
            bwa_aligned_sorted_bam_index = os.path.join(
                config["output"]["classifier"],"bwa_align/{sample}/Aligned.BWA.sortedByCoord.out.bam.bai"),
        input:
            krak2_extracted_bam = os.path.join(
                config["output"]["classifier"],
                "rmhost_extracted_classified_output/{sample}/{sample}_kraken2_extracted_classified.bam"),
            db=rules.bwa_build_Index.output,
            krak_screened_fastq = os.path.join(
                config["output"]["classifier"],
                "rmhost_extracted_classified_output/{sample}/{sample}_kraken2_screen.fastq"),
            krak_screened_r1_fastq = os.path.join(
                config["output"]["classifier"],
                "rmhost_extracted_classified_output/{sample}/{sample}_kraken2_screen_r1.fastq"),
            krak_screened_r2_fastq = os.path.join(
                config["output"]["classifier"],
                "rmhost_extracted_classified_output/{sample}/{sample}_kraken2_screen_r2.fastq")
        params:
            bwa_db_name = os.path.join(
                config["params"]["align"]["bwa"]["db"],
                f"index/{config['params']['project']}/{config['params']['project']}"),
            # bwa_aligned_bam = os.path.join(
            #     config["output"]["classifier"],"bwa_align/{sample}/Aligned.BWA.out.bam"),
        threads: 20
        log:
            os.path.join(config["logs"]["classifier"],
                        "bwa/{sample}/bwa_alignment.log")
        # conda:
        #     "../envs/bowtie2.yaml"
        benchmark:
            os.path.join(config["benchmarks"]["classifier"],
                "bwa/{sample}/bwa_alignment.tsv")
        shell:
            """
            if [ -s "{input.krak_screened_fastq}" ]; then
                bwa mem -t {threads} {params.bwa_db_name} {input.krak_screened_fastq} | samtools sort --threads {threads} > {output.bwa_aligned_sorted_bam}
            else
                bwa mem -t {threads} {params.bwa_db_name} -p {input.krak_screened_r1_fastq} {input.krak_screened_r2_fastq} | samtools sort --threads {threads} > {output.bwa_aligned_sorted_bam}

            fi
            samtools index {output.bwa_aligned_sorted_bam}
            """
    rule bwa_lca_classifier:
        input:
            bwa_aligned_sorted_bam = os.path.join(
                config["output"]["classifier"],"bwa_align/{sample}/Aligned.BWA.sortedByCoord.out.bam"),
            interest_fna = temp(os.path.join(
            config["params"]["align"]["download_dir"],
            f"library/{config['params']['project']}.fna")),
            names_dump = os.path.join(
            config["params"]["align"]["download_dir"],
            "taxonomy/names.dmp"),
            nodes_dump = os.path.join(
            config["params"]["align"]["download_dir"],
            "taxonomy/nodes.dmp"),            
            acc2tax = os.path.join(
                config["params"]["align"]["download_dir"],
                f"acc2tax/{config['params']['project']}_acc2tax.txt"), 

        output:
            lca_profile = os.path.join(
                config["output"]["classifier"],"bwa_align/{sample}/Aligned.BWA.sortedByCoord.out.sam2lca.csv"),
            lca_bam = os.path.join(
                config["output"]["classifier"],"bwa_align/{sample}/Aligned.BWA.sortedByCoord.out.sam2lca.bam"), 
        log:
            os.path.join(config["logs"]["classifier"],
                        "sam2lca/{sample}_sam2lca.log")
        params:
            bwa_output = os.path.join(
                config["output"]["classifier"],"bwa_align","{sample}"),
            base_name = "Aligned_bwa",
            sam2lca_script = config["scripts"]["sam2lca"],
            project = PROJECT
        shell:
            """
            python {params.sam2lca_script} --input {input.bwa_aligned_sorted_bam} --output_bam {output.lca_bam} --output_tsv {output.lca_profile} --nodes {input.nodes_dump} --names {input.names_dump} --seqid_taxid_tsv {input.acc2tax}  --verbose --log_file {log} --check_conserved
            """
    rule bwa_aligned_all:
        input:
            expand(os.path.join(
                config["output"]["classifier"],"bwa_align/{sample}/Aligned.BWA.sortedByCoord.out.sam2lca.bam"),sample=SAMPLES_ID_LIST)

else:
    rule bwa_aligned_all:
        input:

if config["params"]["align"]["bwa2"]["do"]:
    checkpoint calculate_db_chunks:
        input:
            interest_fna = os.path.join(
                config["params"]["align"]["download_dir"],
                "library",f"{config['params']['project']}.fna"),
        output:
            # chunk_fna = temp(os.path.join(
            #     config["params"]["align"]["download_dir"],
            #     "library",config['params']['project'],"chunk_{chunk_num}.fna")),
            chunk_total = os.path.join(
                config["params"]["align"]["download_dir"],
                "library",config['params']['project'],"chunk_num.txt"),
        params:
            chunk_fna_prefix = os.path.join(
                config["params"]["align"]["download_dir"],
                f"library/{config['params']['project']}/chunk"),
        run:
            import os
            from Bio.SeqIO.FastaIO import SimpleFastaParser
            max_usage = 4 * (1024 ** 3)  # 4 GB
            fasta_size = os.stat(input.interest_fna).st_size

            if fasta_size > max_usage:
                # 计算块的数量
                chunk_sum = round(fasta_size / max_usage)
                max_chunk_size = fasta_size / chunk_sum

                # 初始化块
                n = 1
                chunk_fna = params.chunk_fna_prefix + "_" + str(n) + ".fna"
                output_fna = open(chunk_fna, "a")
                # 将fasta文件拆分为块
                with open(input.interest_fna, 'r') as input_fna:
                    for title, seq in SimpleFastaParser(input_fna):
                        file_size = os.stat(chunk_fna).st_size
                        if file_size > max_chunk_size:
                            n += 1
                            output_fna.close()
                            chunk_fna = params.chunk_fna_prefix + "_" + str(n) + ".fna"
                            output_fna = open(chunk_fna, "a")
                        output_fna.write(f'>{title}\n{seq}\n')
                with open(output.chunk_total, "w") as f:
                    f.write(str(n))
            else:
                # 将fasta文件转换为单个块
                n = 1
                chunk_fna = params.chunk_fna_prefix + "_" + str(n) + ".fna"
                shell(f"cp {input.interest_fna} {chunk_fna}")
                with open(output.chunk_total, "w") as f:
                    f.write(str(n))

    rule bwa2_build_Index_chunk:
        output:
            os.path.join(config['params']['align']['bwa2']['db'],"index",config['params']['project'],"chunk_{chunk_num}/chunk_{chunk_num}.amb"),
        input:
            chunk_total = os.path.join(
                config["params"]["align"]["download_dir"],
                "library", config['params']['project'], "chunk_num.txt"),
            chunk_fna = os.path.join(
                config["params"]["align"]["download_dir"],
                "library",config['params']['project'],"chunk_{chunk_num}.fna"),
            fna_list = get_fna_chunks
        params:
            bwa2_db_name = os.path.join(
                config["params"]["align"]["bwa2"]["db"],
                "index",config['params']['project'],"chunk_{chunk_num}/chunk_{chunk_num}"),
        benchmark:
            os.path.join(config["benchmarks"]["classifier"],
                        "bwa2/{chunk_num}_bulid_database_benchmark.tsv")
        resources:
            mem_mb=(
                lambda wildcards, input: os.stat(input.chunk_fna).st_size /1024 /1024 * 5
            ),
        threads: 
            config["resources"]["bwa2"]["threads"]
        conda:
            config["envs"]["bwa2"]
        log:
            os.path.join(config["logs"]["classifier"],
                        "bwa2_db/chunk_{chunk_num}_bwa2_db_build.log")
        shell:
            """
                if [ -s "{input.chunk_fna}" ]; then
                    bwa-mem2 index {input.chunk_fna} -p {params.bwa2_db_name}
                else
                    echo "Error: {input.chunk_fna} is empty or does not exist."
                fi
            """

    rule bwa2_index_all_db_chunks:
        input:
            get_index_db_chunks,
        output:
            done =  os.path.join(config['params']['align']['bwa2']['db'], "index", config['params']['project'], "finish.done")
        shell:
            "touch {output.done}"

    rule bwa2_alignment:
        output:
            bwa_aligned_chunk_sorted_mapped_bam = temp(os.path.join(
                config["output"]["classifier"],"bwa_align/{sample}/Aligned.BWA.chunk_{chunk_num}.sortedByCoord.mapped.out.bam")),
        input:
            krak2_extracted_bam = os.path.join(
                config["output"]["classifier"],
                "rmhost_extracted_classified_output/{sample}/{sample}_kraken2_extracted_classified.bam"),
            bwa_idx = os.path.join(config['params']['align']['bwa2']['db'],"index",config['params']['project'],"chunk_{chunk_num}/chunk_{chunk_num}.amb"),
            krak_screened_fastq = os.path.join(
                config["output"]["classifier"],
                "rmhost_extracted_classified_output/{sample}/{sample}_kraken2_screen.fastq"),
            db_build_done = os.path.join(config['params']['align']['bwa2']['db'], "index", config['params']['project'], "finish.done"),
            krak_screened_r1_fastq = os.path.join(
                config["output"]["classifier"],
                "rmhost_extracted_classified_output/{sample}/{sample}_kraken2_screen_r1.fastq"),
            krak_screened_r2_fastq = os.path.join(
                config["output"]["classifier"],
                "rmhost_extracted_classified_output/{sample}/{sample}_kraken2_screen_r2.fastq"),
        params:
            bwa2_db_name = os.path.join(
                config["params"]["align"]["bwa2"]["db"],
                "index/",config['params']['project'],"chunk_{chunk_num}/chunk_{chunk_num}"),
            bwa_aligned_chunk_sorted_bam = os.path.join(
                config["output"]["classifier"],"bwa_align/{sample}/Aligned.BWA.chunk_{chunk_num}.sortedByCoord.out.bam"),
        resources:
            mem_mb=(
                lambda wildcards, input: os.stat(input.bwa_idx).st_size  /1024 /1024  * 8
            ),
        threads: 
            config["resources"]["bwa2"]["threads"]
        conda:
            config["envs"]["bwa2"]
        log:
            os.path.join(config["logs"]["classifier"],
                        "bwa/{sample}/bwa_chunk_{chunk_num}_alignment.log")
        benchmark:
            os.path.join(config["benchmarks"]["classifier"],
                "bwa/{sample}/bwa_{chunk_num}_alignment.tsv")
        shell:
            """
            if [ -s "{input.krak_screened_fastq}" ]; then
                bwa-mem2 mem -t {threads} {params.bwa2_db_name} {input.krak_screened_fastq} | samtools sort --threads {threads} -o {params.bwa_aligned_chunk_sorted_bam}
            else
                bwa-mem2 mem -t {threads} {params.bwa2_db_name} -p {input.krak_screened_r1_fastq} {input.krak_screened_r2_fastq} | samtools sort --threads {threads} -o {params.bwa_aligned_chunk_sorted_bam}

            fi
            samtools view --threads {threads} -F 4 {params.bwa_aligned_chunk_sorted_bam} -o {output.bwa_aligned_chunk_sorted_mapped_bam}
            """

    rule bwa2_merge_db_alignments:
        input:
            chunk_aligned_bam = get_db_chunk_alignments,
        output:
            bwa_aligned_sorted_mapped_bam = os.path.join(
                config["output"]["classifier"],"bwa_align/{sample}/Aligned.BWA.sortedByCoord.mapped.out.bam"),
            bwa_aligned_sorted_mapped_bam_index = os.path.join(
                config["output"]["classifier"],"bwa_align/{sample}/Aligned.BWA.sortedByCoord.mapped.out.bam.bai"),
        log:
            os.path.join(config["logs"]["classifier"],
                        "bwa/{sample}/bwa_merge_alignment.log")
        threads: 
            config["resources"]["bwa2"]["threads"]
        resources:
            # mem_mb=(
            #     lambda wildcards, input :max([os.stat(f).st_size / 1024 / 1024 * 2 for f in set(input.chunk_aligned_bam)])
            # )
            mem_mb=5000
        shell:
            """
            samtools merge --threads {threads} -f {output.bwa_aligned_sorted_mapped_bam} {input.chunk_aligned_bam} 2> {log}
            samtools index {output.bwa_aligned_sorted_mapped_bam}
            """
    rule bwa2_lca_classifier:
        input:
            bwa_aligned_sorted_mapped_bam = os.path.join(
                config["output"]["classifier"],"bwa_align/{sample}/Aligned.BWA.sortedByCoord.mapped.out.bam"),
            names_dump = os.path.join(
            config["params"]["align"]["download_dir"],
            "taxonomy/names.dmp"),
            nodes_dump = os.path.join(
            config["params"]["align"]["download_dir"],
            "taxonomy/nodes.dmp"),            
            acc2tax = os.path.join(
                config["params"]["align"]["download_dir"],
                "acc2tax/",f"{config['params']['project']}_acc2tax.txt"), 
        output:
            lca_profile = os.path.join(
                config["output"]["classifier"],"bwa_align/{sample}/Aligned.BWA.sortedByCoord.out.sam2lca.csv"),
            lca_bam = os.path.join(
                config["output"]["classifier"],"bwa_align/{sample}/Aligned.BWA.sortedByCoord.out.sam2lca.bam"), 
        params:
            bwa_output = os.path.join(
                config["output"]["classifier"],"bwa_align","{sample}"),
            sam2lca_script = config["scripts"]["sam2lca"],
            project = config["params"]["project"],
        resources:
            mem_mb=config["resources"]["krak2_matrix_build"]["mem_mb"]
        benchmark:
            os.path.join(config["benchmarks"]["classifier"],
                "bwa/{sample}/bwa_assigned.tsv")
        conda:
            config["envs"]["kmer_python"]
        log:
            os.path.join(config["logs"]["classifier"],
                        "sam2lca/{sample}_sam2lca.log")
        shell:
            """
            python {params.sam2lca_script} --input {input.bwa_aligned_sorted_mapped_bam} --output_bam {output.lca_bam} --output_tsv {output.lca_profile} --nodes {input.nodes_dump} --names {input.names_dump} --seqid_taxid_tsv {input.acc2tax}  --verbose --log_file {log}
            """
    rule bwa2_matrix_build:
        input:
            lca_bam = os.path.join(
                config["output"]["classifier"],"bwa_align/{sample}/Aligned.BWA.sortedByCoord.out.sam2lca.bam"),
            unmapped_bam_sorted_file =os.path.join(
                config["output"]["host"],
                "unmapped_host/{sample}/Aligned_sortedByName_unmapped_out.bam"),
            names_dump = os.path.join(
            config["params"]["align"]["download_dir"],
            "taxonomy/names.dmp"),
            nodes_dump = os.path.join(
            config["params"]["align"]["download_dir"],
            "taxonomy/nodes.dmp"),   
        output:
            profile_tsv = os.path.join(
                config["output"]["profile"],
                "{sample}/microbiome_out/microbiome_profile.tsv"), 
            barcode_file = os.path.join(
                config["output"]["profile"],
                "{sample}/microbiome_out/barcodes.tsv"),
            matrix_file = os.path.join(
                config["output"]["profile"],
                "{sample}/microbiome_out/matrix.mtx"),
            feature_file = os.path.join(
                config["output"]["profile"],
                "{sample}/microbiome_out/features.tsv"),
        params:
            bam2mtx_script = config["scripts"]["bam2mtx"],
        resources:
            mem_mb=config["resources"]["krak2_matrix_build"]["mem_mb"]
        log:
            os.path.join(config["logs"]["classifier"],
                        "matrix/{sample}_martix_build.log")
        conda:
            config["envs"]["kmer_python"]
        shell:
            """
            python {params.bam2mtx_script} --cb_bam {input.unmapped_bam_sorted_file} --align_bam {input.lca_bam} --nodes {input.nodes_dump} --names {input.names_dump} --profile_tsv {output.profile_tsv} --matrixfile {output.matrix_file} --cellfile {output.barcode_file} --taxfile {output.feature_file}  --log_file {log}
            """
    rule bwa2_aligned_all:
        input:
            expand(os.path.join(
                config["output"]["profile"],
                "{sample}/microbiome_out/microbiome_profile.tsv"),sample=SAMPLES_ID_LIST)
else:
    rule bwa2_aligned_all:
        input:

if config["params"]["align"]["minimap2"]["do"]:
    # rule minimap2_build_Index:
    #     output:
    #         minimap2_db = os.path.join(
    #             config["params"]["align"]["minimap2"]["db"],
    #             f"index/{config['params']['project']}/{config['params']['project']}.mmi"),
    #     input:
    #         interest_fna = os.path.join(
    #             config["params"]["align"]["download_dir"],
    #             f"library/{config['params']['project']}.fna"),
    #     params:
    #         bwa_db_name = os.path.join(
    #             config["params"]["align"]["bwa"]["db"],
    #             f"index/{config['params']['project']}/{config['params']['project']}")
    #     # conda:
    #     #     "../envs/bowtie2.yaml"
    #     threads: 20
    #     log:
    #         os.path.join(config["logs"]["classifier"],
    #                     "bwa_db/bwa_db_build.log")
    #     shell:
    #         """
    #         minimap2 -ax sr -t 20 -d {output.minimap2_db} {input.interest_fna}
    #         """
    rule minimap2_alignment:
        output:
            minimap2_aligned_sorted_bam = os.path.join(
                config["output"]["classifier"],"minimap2_align/{sample}/Aligned.minimap2.sortedByCoord.out.bam"),
            minimap2_aligned_sorted_bam_index = os.path.join(
                config["output"]["classifier"],"minimap2_align/{sample}/Aligned.minimap2.sortedByCoord.out.bam.bai"),
        input:
            krak2_extracted_bam = os.path.join(
                config["output"]["classifier"],
                "rmhost_extracted_classified_output/{sample}/{sample}_kraken2_extracted_classified.bam"),
            interest_fna = os.path.join(
                config["params"]["align"]["download_dir"],
                "library/",f"{config['params']['project']}.fna"),
            krak_screened_fastq = os.path.join(
                config["output"]["classifier"],
                "rmhost_extracted_classified_output/{sample}/{sample}_kraken2_screen.fastq"),
            krak_screened_r1_fastq = os.path.join(
                config["output"]["classifier"],
                "rmhost_extracted_classified_output/{sample}/{sample}_kraken2_screen_r1.fastq"),
            krak_screened_r2_fastq = os.path.join(
                config["output"]["classifier"],
                "rmhost_extracted_classified_output/{sample}/{sample}_kraken2_screen_r2.fastq")
        threads: 20
        log:
            os.path.join(config["logs"]["classifier"],
                        "minimap2/{sample}/minimap2_alignment.log")
        # conda:
        #     "../envs/bowtie2.yaml"
        benchmark:
            os.path.join(config["benchmarks"]["classifier"],
                "minimap2/{sample}/minimap2_alignment.tsv")
        resources:
            mem_mb=(
                lambda wildcards: os.stat(os.path.join(config["params"]["align"]["download_dir"],
                f"library/{config['params']['project']}.fna")).st_size  /1024 /1024  * 6
            ),
        shell:
            """
            if [ -s "{input.krak_screened_fastq}" ]; then
                minimap2 -ax sr -A2 -B2 -O4,24 -E2,1 -k10 -w8 -t {threads} {input.interest_fna} {input.krak_screened_fastq}  | samtools sort --threads {threads} -o  {output.minimap2_aligned_sorted_bam}
            else
                minimap2 -ax sr -A2 -B2 -O4,24 -E2,1 -k10 -w8 -t {threads} {input.interest_fna} -p {input.krak_screened_r1_fastq} {input.krak_screened_r2_fastq}  | samtools sort --threads {threads} -o {output.minimap2_aligned_sorted_bam}

            fi

            samtools index {output.minimap2_aligned_sorted_bam}
            """
    rule minimap2_lca_classifier:
        input:
            minimap2_aligned_sorted_bam = os.path.join(
                config["output"]["classifier"],"minimap2_align/{sample}/Aligned.minimap2.sortedByCoord.out.bam"),
            interest_fna = os.path.join(
            config["params"]["align"]["download_dir"],
            f"library/{config['params']['project']}.fna"),
            names_dump = os.path.join(
            config["params"]["align"]["download_dir"],
            "taxonomy/names.dmp"),
            nodes_dump = os.path.join(
            config["params"]["align"]["download_dir"],
            "taxonomy/nodes.dmp"),            
            acc2tax = os.path.join(
                config["params"]["align"]["download_dir"],
                f"acc2tax/{config['params']['project']}_acc2tax.txt"), 
        output:
            lca_profile = os.path.join(
                config["output"]["classifier"],"minimap2_align/{sample}/Aligned.minimap2.sortedByCoord.out.sam2lca.csv"),
            lca_bam = os.path.join(
                config["output"]["classifier"],"minimap2_align/{sample}/Aligned.minimap2.sortedByCoord.out.sam2lca.bam"), 
        params:
            minimap2_output = os.path.join(
                config["output"]["classifier"],"minimap2_align","{sample}"),
            sam2lca_script = config["scripts"]["sam2lca"],
            project = PROJECT
        resources:
            mem_mb=config["resources"]["krak2_matrix_build"]["mem_mb"]
        benchmark:
            os.path.join(config["benchmarks"]["classifier"],
                "minimap2/{sample}/minimap2_assigned.tsv")
        conda:
            config["envs"]["kmer_python"]
        log:
            os.path.join(config["logs"]["classifier"],
                        "sam2lca/{sample}_sam2lca.log")
        shell:
            """
            python {params.sam2lca_script} --input {input.minimap2_aligned_sorted_bam} --output_bam {output.lca_bam} --output_tsv {output.lca_profile} --nodes {input.nodes_dump} --names {input.names_dump} --seqid_taxid_tsv {input.acc2tax}  --verbose --log_file {log}
            """
    rule minimap2_matrix_build:
        input:
            lca_bam = os.path.join(
                config["output"]["classifier"],"minimap2_align/{sample}/Aligned.minimap2.sortedByCoord.out.sam2lca.bam"),
            unmapped_bam_sorted_file =os.path.join(
                config["output"]["host"],
                "unmapped_host/{sample}/Aligned_sortedByName_unmapped_out.bam"),
            names_dump = os.path.join(
            config["params"]["align"]["download_dir"],
            "taxonomy/names.dmp"),
            nodes_dump = os.path.join(
            config["params"]["align"]["download_dir"],
            "taxonomy/nodes.dmp"),   
        output:
            profile_tsv = os.path.join(
                config["output"]["profile"],
                "{sample}/microbiome_out/microbiome_profile.tsv"), 
            barcode_file = os.path.join(
                config["output"]["profile"],
                "{sample}/microbiome_out/barcodes.tsv"),
            matrix_file = os.path.join(
                config["output"]["profile"],
                "{sample}/microbiome_out/matrix.mtx"),
            feature_file = os.path.join(
                config["output"]["profile"],
                "{sample}/microbiome_out/features.tsv"),
        params:
            bam2mtx_script = config["scripts"]["bam2mtx"],
        resources:
            mem_mb=config["resources"]["krak2_matrix_build"]["mem_mb"]
        log:
            os.path.join(config["logs"]["classifier"],
                        "matrix/{sample}_martix_build.log")
        conda:
            config["envs"]["kmer_python"]
        shell:
            """
            python {params.bam2mtx_script} --cb_bam {input.unmapped_bam_sorted_file} --align_bam {input.lca_bam} --nodes {input.nodes_dump} --names {input.names_dump} --profile_tsv {output.profile_tsv} --matrixfile {output.matrix_file} --cellfile {output.barcode_file} --taxfile {output.feature_file}  --log_file {log}
            """
    rule minimap2_aligned_all:
        input:
            expand(os.path.join(
                config["output"]["profile"],
                "{sample}/microbiome_out/microbiome_profile.tsv"),sample=SAMPLES_ID_LIST)
else:
    rule minimap2_aligned_all:
        input:

rule align_all:
    input:
        rules.bowtie2_aligned_all.input,
        rules.bwa_aligned_all.input,
        rules.bwa2_aligned_all.input,
        rules.minimap2_aligned_all.input,