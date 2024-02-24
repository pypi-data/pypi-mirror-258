import nbformat


class NBMeta:
    def __init__(self):
        pass

    @staticmethod
    def get_nbformat():
        return nbformat.current_nbformat

    @staticmethod
    def get_nbformat_minor():
        return nbformat.current_nbformat_minor

    @staticmethod
    def get_notebook_content():
        return (
                '{\n'
                ' "cells": [],\n'
                ' "metadata": {},\n'
                ' "nbformat": ' + str(NBMeta.get_nbformat()) + ',\n'
                ' "nbformat_minor": ' + str(NBMeta.get_nbformat_minor()) + '\n'
        )
