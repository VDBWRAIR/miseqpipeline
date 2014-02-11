def label_N( stats, minbq ):
    '''
        Labels all qualities < minbq as N

        @param stats - Stats dictionary returned from stats_at_refpos.stats
        @param minbq - The mininum base quality to determine if a quality should belong to N

        @returns stats dictionary with baseq subkey for each base in the dictionary.
    '''
    stats2 = {}
    stats2['depth'] = stats['depth']
    stats2['mqualsum'] = stats['mqualsum']
    stats2['bqualsum'] = stats['bqualsum']


    for base, quals in stats.iteritems():
            # Only interested in base stats in this loop
            if base not in ('depth','mqualsum','bqualsum'):

            # generates a list called bquals
            bquals = quals['baseq']
            

            # loop to examine the quality score and identifyes bases with a quality score less than the minbq of 25
            for q in bquals:
                k = base
                if q < minbq:
                    k = 'N'

                # adds the N to the nucleotides (A C G T and N)
                if k not in stats2:
                    stats2[k] = {'baseq':[]}
                    stats2[k] ['baseq'].append( q )


    return stats2



def caller( bamfile, refstr, minbq, maxd, mind=10, minth=0.8 ):
    '''
        Calls a given base at refstr inside of bamfile. At this time refstr has to be a single
        base position. The base is determined by first labeling all bases less than minbq as N and then
        determining if the depth is < mind or >= mind.
        If < and the % of N is > minth then call it an N as it is the majority.
        If >= 10 then remove all N

        The final stage is to call call_on_pct with the remaining statistics

        @param bamfile - Path to a bamfile
        @param refstr - Region string acceptable for samtools
        @param minbq - Minimum base quality to determine if it is low quality or not to call it an N
        @param maxd - Maximum depth in the pileup to allow
        @param mind - Minimum depth threshold
        @param minth - Minimum percentage for an base to be called non ambigious

        @returns one of the items from the set( 'ATGCMRWSYKVHDBN' )
    '''
    # call the nucleotides

    stats = stats(bamfile, regionstr, minmq, minbq, maxd):
    stast2 = label_N(stats, minbq)


    # if the quality is 25 or greater ignore the N bases
    if stats2['depth'] >= mindp:
        del stats2['N']

    else:
        # defines if the base is an N
        np = len(stats2['N']['baseq'])/(stats2['depth']*1.0)
        if np > (1-min_th):
            return 'N'

    return call_on_pct(stats2, min_th)




def call_on_pct( stats, minth=0.8 ):
    '''
        Calls a base from the given stats dictionary if it is the majority. A majority base is
        any base where it is in %total >= minth.

        @param stats2 - Stats dictionary returned from label_N or stats_at_refpos.stats
        @param minth - minimum percentage that a base needs to be present in order to be called non-ambiguous

        @returns the called base based on the percentages in the given stats
    '''
    

    nt_list = []


    stats = stats(bamfile, regionstr, minmq, minbq, maxd):
    stats2 = label_N(stats, minbq)

        for base, quals in stats.iteritems():
            # Only interested in base stats in this loop
            if base not in ('depth','mqualsum','bqualsum'):

            # generates a list called bquals
            bquals = quals['baseq']

            for q in bquals:
                k = base

                np_2 = len(stats2[base]['baseq'])/(stats2['depth']*1.0)
                    if np_2 > (1-minth):
                        return base





    dnalist = ''.join(sorted(nt_list))


def iupac_amb( dnalist ):

    return (iupac.get(dnalist))







