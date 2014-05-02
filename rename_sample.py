#!/usr/bin/env python

import os
import sys
import re
from glob import glob
from os.path import *
import argparse
import data
import shutil

'''
    Traverse backwards through the NGSData structure starting
    with rbsfile which should be a symlink to ReadData(although sometimesit is RawData)
    and rename all files involved
'''

def main( args ):
    preads = get_reads( args.ngsdata, args.origname )
    funcs = {
        'Sanger': rename_sanger,
        'MiSeq': rename_miseq,
        'Roche454': rename_roche
    }
    for p, reads in preads.iteritems():
        for rs in reads:
            # Miseq returns tuple of paired read so normalize here
            if not isinstance(rs,tuple):
                rs = [rs]
            for r in rs:
                print r
                funcs[p]( r, args.origname, args.newname, args.ngsdata )

def get_reads( ngsdata, samplename ):
    rbs = join( ngsdata, 'ReadsBySample' )
    rbsdir = join( rbs, samplename )
    platreads = data.reads_by_plat( rbsdir )
    return platreads

def rename_roche( rbsfile, old, new, ngsdata ):
    rund, readp = runread_path( os.readlink(rbsfile), 'Roche454' )
    rbsd = dirname(rbsfile)

    newrbsd = join( dirname(rbsd), new )
    if not isdir( newrbsd ):
        os.mkdir( newrbsd )
    rename_file( rbsfile, old, new )

def rename_miseq( rbsfile, old, new, ngsdata ):
    '''
        Rename files
    '''
    rund, readp = runread_path( os.readlink(rbsfile), 'MiSeq' )
    rawd = join( ngsdata, 'RawData', 'MiSeq', rund )
    rbsd = dirname( rbsfile )
    bcdir = join( rawd, 'Data', 'Intensities', 'BaseCalls' )
    # Raw file is fastq.gz without the date before it
    rawfilename = re.sub( '_\d{4}_\d{2}_\d{2}.fastq', '.fastq.gz', readp )
    rawfile = join( bcdir, rawfilename )
    newrbsd = join( dirname(rbsd), new )
    if not isdir( newrbsd ):
        os.mkdir( newrbsd )
    # Rename link and link dest
    rename_file( rbsfile, old, new )
    # Rename the rawfile
    rename_file( rawfile, old, new )

def rename_sanger( rbsfile, old, new, ngsdata ):
    '''
        Rename RBS, Read, Raw
    '''
    lnkdst = os.readlink( rbsfile )
    rund, readp = runread_path( lnkdst, 'Sanger' )
    # NGSData/ReadsBySample/samplename
    rbsd = dirname( rbsfile )
    # samplename
    samplename = basename( rbsd )
    # NGSData/ReadData/Sanger/rund
    readd = join( ngsdata, 'ReadData', 'Sanger', rund )
    # NGSData/RawData/Sanger/rund
    rawd = join( ngsdata, 'RawData', 'Sanger', rund )

    rawfile = join( rawd, readp )
    readfile = join( readd, readp )

    # Recursively rename
    newrbsd = join( dirname(rbsd), new )
    if not isdir( newrbsd ):
        os.mkdir( newrbsd )
    rename_file( rbsfile, old, new )

def resolve_symlink( path ):
    '''
        Resolves symlinks as they may be relative paths and such
        @param path - Symlink location such that os.readlink(path) works as expected
    '''
    if not exists( path ):
        raise OSError( '{} does not exist or is a broken link'.format(path) )

    if not islink( path ):
        return path

    sympath = os.readlink( path )
    d = os.getcwd()
    sdir = normpath( dirname( path ) )
    os.chdir( sdir )
    apath = abspath( sympath )
    os.chdir( d )
    resolved = relpath( apath )
    return resolved

def rename_file( path, find, replace ):
    '''
        Replace find in path with replace

        If path is a symlink then replace both the symlink and the file it points to
    '''
    if isdir(dirname(path)):
        newp = path.replace( os.sep+find, os.sep+replace )
    else:
        newp = path.replace( find, replace )
    if os.path.islink( path ):
        # Resolve the symlink correctly
        # resolves relative to this directory
        spath = resolve_symlink( path )
        # Replace the dst of link
        nf = rename_file( spath, find, replace )
        # Now make it relative to where path was
        nf = relpath( nf, dirname(path) )
        os.unlink( path )
        os.symlink( nf, newp )
    elif os.path.isfile( path ):
        shutil.move(path,newp)
    else:
        raise Exception("{} is not a valid path".format(path))
    return newp

def runread_path( path, platform ):
    _, run_read = path.split(platform)
    parts = run_read[1:].split(os.sep)
    run = parts[0]
    if len(parts) > 1:
        read = os.sep.join(parts[1:])
    else:
        read = parts[1]
    return run,read

def parse_args( args=sys.argv[1:] ):
    parser = argparse.ArgumentParser(
        description='''Renames sequence files'''
    )

    parser.add_argument(
        'origname',
        help='Original samplename'
    )

    parser.add_argument(
        'newname',
        help='New name to rename to'
    )

    ngsdata='/home/EIDRUdata/NGSData'
    parser.add_argument(
        '--ngsdata',
        default=ngsdata,
        help='Path to NGSData[Default: {}]'.format(ngsdata)
    )

    return parser.parse_args( args )

if __name__ == '__main__':
    main(parse_args())
